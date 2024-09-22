import os

import psycopg2
import openai
import azure.identity
import numpy as np
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

load_dotenv()
# Environment variables for database connection
DBUSER = os.environ["DBUSER"]
DBPASS = os.environ["DBPASS"]
DBHOST = os.environ["DBHOST"]
DBNAME = os.environ["DBNAME"]

# Use SSL if not connecting to localhost
DBSSL = "disable"
if DBHOST != "localhost":
    DBSSL = "require"

# Connect to the PostgreSQL database
conn = psycopg2.connect(database=DBNAME, user=DBUSER, password=DBPASS, host=DBHOST, sslmode=DBSSL)
conn.autocommit = True
cur = conn.cursor()
# Enable pgvector extension
register_vector(conn)
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

# Add an embedding column to the table
# cur.execute("ALTER TABLE videos ADD COLUMN embedding vector(256)")
cur.execute("CREATE INDEX ON videos USING hnsw (embedding vector_l2_ops)")

# For each row in the table, compute an embedding using an embedding model
cur.execute("SELECT * FROM videos ORDER BY title DESC")

rows = cur.fetchall()

for row in rows:
    if row[3] is not None:
        continue
    string_to_embed = row[0] + " " + row[1]
    # Compute the embedding for the string

    credential = azure.identity.DefaultAzureCredential()
    token_provider = azure.identity.get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )

    client = openai.AzureOpenAI(
        api_version="2024-03-01-preview",
        azure_endpoint="https://cog-xw55anu4yrb3k.openai.azure.com",
        azure_ad_token_provider=token_provider,
    )

    response = client.embeddings.create(
        # Azure OpenAI takes the deployment name as the model name
        model="emb3sm",
        input=string_to_embed,
        dimensions=256,
    )
    embedding = response.data[0].embedding
    embedding = np.array(embedding)
    # Update the row with the computed embedding
    cur.execute("UPDATE videos SET embedding = %s WHERE id = %s", (embedding, row[0]))
    print(f"Updated embedding for {row[1]}")

# Close the cursor and connection
cur.close()
conn.close()
