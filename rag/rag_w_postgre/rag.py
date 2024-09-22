"""
Simple RAG:

1. Setup postgres connection
2. Get question from user
3. Use question to search Postgres table
4. Format the results in an LLM-friendly way
5. Send the results to the LLM

Advanced RAG:

1. Get question from user
2. Use LLM to turn question into a good search query
...
"""

import os

import numpy as np
# the following is needed for using hosted models on Github Marketplace 
# but requires access
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
# python specific package to interact with postgre
import psycopg2
# using the pgvector to make DB accept vector data types
from pgvector.psycopg2 import register_vector
from dotenv import load_dotenv

# Set up GitHub models
endpoint = "https://models.inference.ai.azure.com"
model_name = "text-embedding-3-small"
# needs to be manually added if it isn't being used with github codespace
token = os.environ["GITHUB_TOKEN"]

# Set up Postgres
load_dotenv(override=True)
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]
# Use SSL if not connecting to localhost
DBSSL = "disable"
if DBHOST != "localhost":
    DBSSL = "require"

conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, sslmode=DBSSL)
# each SQL statement is automatically committed meaning that the changes 
# to the DB is visible immediately; also used for SELECT queries which 
# don't change the DB records and it can improve performance by reducting 
# the overhead of transaction management
conn.autocommit = True
cur = conn.cursor()
# enabling the DB vector operations and store vector data
register_vector(conn)
# use the pgvector extension in DB
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

# Get question from user
question = "is it possible to build custom chat participant for github copilot?"

# Use question to search Postgres table using LIKE operator on title/description
# this is keyword search which contains the question substring because 
# it is searching for "%{question}%" where the "%" is equivalent to "*" in regex

# cur.execute(
#     "SELECT * FROM videos WHERE title LIKE %s OR description LIKE %s LIMIT 10", (f"%{question}%", f"%{question}%")
# )
# results = cur.fetchall()
# for result in results:
    # prints all the titles in the results; one can return whatever else one wants
#    print(result[1])

# Use question to search Postgres table using built-in full text search to_tsvector
# cur.execute(
#    "SELECT * FROM videos WHERE to_tsvector(title || ' ' || description) @@ to_tsquery(%s) LIMIT 10", (question,)
# )
# results = cur.fetchall()
# for result in results:
#    print(result[1])

# the following query ranks the full text search query by using
# cover density ranking(postgre specific ranking)
# cur.execute(
#     """
#     SELECT id, title, description
#         FROM videos, plainto_tsquery('english', %(query)s) query
#         WHERE to_tsvector('english', description) @@ query
#         ORDER BY ts_rank_cd(to_tsvector('english', description), query) DESC
#         LIMIT 10
#     """,
#     {"query": question},
# )
# results = cur.fetchall()
# for result in results:
#     print(result[1])
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# TO DO VECTOR SEARCH

# Turn the question into an embedding
# using the github marketplace model and Azurekeycredential since it's hosted on azure
client = EmbeddingsClient(endpoint=endpoint, credential=AzureKeyCredential(token))

# change the dimensions if you don't need such high dimensions 
# but MAKE SURE THAT THE DIMENSIONS ARE IDENTICAL TO THE STORED VECTOR DIMENSION in the DB
# `embed_videos.py`, creates the embeddings in the DB
response = client.embed(input=question, model=model_name, dimensions=256)
# the embedding needs to be converted to a numpy array always
# the data[0] is for referencing the embedding of the sentence, as the model supports 
# batch encoding, the data is subscriptable
embedding = np.array(response.data[0].embedding)

# Do a Postgres vector embedding search on embedding column with euclidean operator
# this is only the vector/embedding search
# there are a bunch of operators, which pgvector supports
# https://github.com/pgvector/pgvector?tab=readme-ov-file#vector-operators

# cur.execute("SELECT id, title, description FROM videos ORDER BY embedding <-> %s LIMIT 10", (embedding,))
# results = cur.fetchall()
# for result in results:
#     print(result[1])

# uses the cosine distance operator with hybrid search feature as it gives the best results
# more on hybrid search results 
# https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/azure-ai-search-outperforming-vector-search-with-hybrid/ba-p/3929167
cur.execute(
    """
WITH semantic_search AS (
    SELECT id, RANK () OVER (ORDER BY embedding <=> %(embedding)s) AS rank
    FROM videos
    ORDER BY embedding <=> %(embedding)s
    LIMIT 20
),
keyword_search AS (
    SELECT id, RANK () OVER (ORDER BY ts_rank_cd(to_tsvector('english', title || ' ' || description), query) DESC)
    FROM videos, plainto_tsquery('english', %(query)s) query
    WHERE to_tsvector('english', title || ' ' || description) @@ query
    ORDER BY ts_rank_cd(to_tsvector('english', title || ' ' || description), query) DESC
    LIMIT 20
)
# the below part uses `reciprocal rank fusion` to order the results; one of the ranking 
SELECT
    COALESCE(semantic_search.id, keyword_search.id) AS id,
    COALESCE(1.0 / (%(k)s + semantic_search.rank), 0.0) +
    COALESCE(1.0 / (%(k)s + keyword_search.rank), 0.0) AS score
FROM semantic_search
FULL OUTER JOIN keyword_search ON semantic_search.id = keyword_search.id
ORDER BY score DESC
LIMIT 20
""",
    {"query": question, "embedding": embedding, "k": 60},
)
# more on reciprocal rank fusion(RRF) https://learn.microsoft.com/en-us/azure/search/vector-search-ranking#reciprocal-rank-fusion-rrf-for-hybrid-queries

results = cur.fetchall()

# Fetch the videos by ID
ids = [result[0] for result in results]
cur.execute("SELECT id, title, description FROM videos WHERE id = ANY(%s)", (ids,))
results = cur.fetchall()
for result in results:
    print(result[1])

# Format the results for the LLM; using the markdown headers to format
formatted_results = ""
for result in results:
    formatted_results += f"## {result[1]}\n\n{result[2]}\n"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage(
            content="You must answer user question according to sources. Say you dont know if you cant find answer in sources. Cite the title of each video inside square brackets. The title of each video which will be a markdown heading."
        ),
        UserMessage(content=question + "\n\nSources:\n\n" + formatted_results),
    ],
    model="gpt-4o",
    temperature=0.3,
    max_tokens=1000,
    top_p=1.0
)

print("Answer:\n\n")
print(response.choices[0].message.content)
# to close the DB connection
# cur.close()
# conn.close()
