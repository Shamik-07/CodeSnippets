
from typing import Dict, List
from autogen import ConversableAgent
import sys
import os
from dotenv import load_dotenv
from collections import defaultdict
from pathlib import Path
import math


_ = load_dotenv()

with open(Path(__file__).resolve().parent/"restaurant-data.txt",'r') as f:
    txt = f.readlines()
    restaurant_reviews = defaultdict(list)
    for line in txt:
        restaurant,review=line.split(".", maxsplit=1)
        restaurant_reviews[restaurant].append(review)

def fetch_restaurant_data(restaurant_name: str) -> Dict[str, List[str]]:
    # TODO
    # This function takes in a restaurant name and returns the reviews for that restaurant.
    # The output should be a dictionary with the key being the restaurant name and the value being a list of reviews for that restaurant.
    # The "data fetch agent" should have access to this function signature, and it should be able to suggest this as a function call.
    # Example:
    # > fetch_restaurant_data("Applebee's")
    # {"Applebee's": ["The food at Applebee's was average, with nothing particularly standing out.", ...]}
    restaurant_reviews_copy = restaurant_reviews.copy()
    return {restaurant_name:restaurant_reviews[restaurant_name]}


def calculate_overall_score(restaurant_name: str, food_scores: List[int], customer_service_scores: List[int]) -> Dict[str, float]:
    # TODO
    # This function takes in a restaurant name, a list of food scores from 1-5, and a list of customer service scores from 1-5
    # The output should be a score between 0 and 10, which is computed as the following:
    # SUM(sqrt(food_scores[i]**2 * customer_service_scores[i]) * 1/(N * sqrt(125)) * 10
    # The above formula is a geometric mean of the scores, which penalizes food quality more than customer service. 
    # Example:
    # > calculate_overall_score("Applebee's", [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    # {"Applebee's": 5.048}
    # NOTE: be sure to that the score includes AT LEAST 3  decimal places. The public tests will only read scores that have 
    # at least 3 decimal places.
    final_score = sum(math.sqrt(i[0]**2 * i[1])/(len(food_scores)*math.sqrt(125))
                      for i in zip(food_scores,customer_service_scores)) * 10
    return {restaurant_name:f"{final_score:.3f}"}

def get_data_fetch_agent_prompt(restaurant_query: str) -> str:
    # TODO
    # It may help to organize messages/prompts within a function which returns a string. 
    # For example, you could use this function to return a prompt for the data fetch agent 
    # to use to fetch reviews for a specific restaurant.
    pass

# TODO: feel free to write as many additional functions as you'd like.

# Do not modify the signature of the "main" function.
def main(user_query: str):
    entrypoint_agent_system_message = """You are a helpful assistant who calculates the overall score of a given restaurant.
    If you are asked any other query other than this you don't answer and return 'TERMINATE'.
    If the data to answer the query isn't available then you return 'TERMINATE'.
    Don't provide any other information other than what's asked of you.
    When you have finished you return 'TERMINATE'.""" # TODO
    # example LLM config for the entrypoint agent
    llm_config = {"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API_KEY")}]}

    # the main entrypoint/supervisor agent
    entrypoint_agent = ConversableAgent("entrypoint_agent", 
                                        system_message=entrypoint_agent_system_message, 
                                        llm_config=False,
                                    human_input_mode="NEVER",
                                   is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],)
    entrypoint_agent.register_for_execution(name="fetch_restaurant_data")(fetch_restaurant_data)
    entrypoint_agent.register_for_execution(name="calculate_overall_score")(calculate_overall_score)


    datafetch_agent = ConversableAgent("datafetch_agent", llm_config=llm_config,
    system_message="""You fetch the restaurant reviews data and return all data.
    Don't provide any other information other than what's asked of you.
    Return 'TERMINATE' when you are done.""",
                                       human_input_mode="NEVER",
                                      is_termination_msg=lambda msg: "terminate" in msg.get("content").lower())
    datafetch_agent.register_for_llm(name="fetch_restaurant_data",
                                     description="Fetches the reviews for a specific restaurant.")(fetch_restaurant_data)
    restaurantscore_agent = ConversableAgent("restaurantscore_agent", llm_config=llm_config,
                                             system_message="""You calculate the score for a given restaurant.
                                            Don't provide any other information other than what's asked of you.
                                            Return 'TERMINATE' when you are done.""",
                                             human_input_mode="NEVER",
                                      is_termination_msg=lambda msg: "terminate" in msg.get("content").lower())
    restaurantscore_agent.register_for_llm(name="calculate_overall_score",
                                     description="Fetches the score for a specific restaurant.")(calculate_overall_score)

    result = entrypoint_agent.initiate_chats([
        {
      "recipient":entrypoint_agent,
        "message":rf"""{user_query}
        Identify the restaurant name in the query above and match it to one of the following names:
        {restaurant_reviews.keys()}. Rewrite the query by changing only the restaurant name to one matching in the list.
        If the restaurant isn't present in the list of restaurant names given, then return 'TERMINATE'.
        """,
        "max_turns":1,
    },
        {
            "recipient":datafetch_agent,
            "message":"""Take the query and answer.

             Each restaurant will have the reviews in the following pattern: {'restaurant_name':
             [review_1,review_2,...,review_n ]}.
             Count the total number of reviews, it's the length of the list, and store it in a variable
              called 'total_reviews'.
             Each review will have two sentences.
             The first sentence will be the food_review and the second one the customer_service_review.

             To rank each food_review and customer_service_review, look for keywords in the review.
             Each review has *keyword adjectives* that correspond to the score that the restaurant should 
             get for its food_review and customer_service_review. Here are the keywords the agent should look out for:
             ```
             Score 1/5 has one of these adjectives: awful, horrible, or disgusting.
             Score 2/5 has one of these adjectives: bad, unpleasant, or offensive.
             Score 3/5 has one of these adjectives: average, uninspiring, or forgettable.
             Score 4/5 has one of these adjectives: good, enjoyable, or satisfying.
             Score 5/5 has one of these adjectives: awesome, incredible, or amazing.
             ```
             You return the results in the following JSON format: {'restaurant_name': 'abc','total_reviews':n,
               'food_reviews': [1,2,3,...,n],
               'customer_service_reviews:[1,2,3,...,n]}.

             The 'total_reviews'MUST match the total number of food reviews
              and the total number of customer service reviews.
             Don't provide any other information other than what's asked.""",
             "max_turns":2,
             "summary_method":"last_msg"
        },
        {
            "recipient":restaurantscore_agent,
            "message":"""You will be given a JSON object in the following structure:
            {'restaurant_name': 'abc','total_reviews':n,
           'food_reviews': [1,2,3,...,n],
           'customer_service_reviews:[1,2,3,...,n]}.
           You have to calcuate the overall_score of the restaurant based on the information given.
           You return "The overall score for "restaurant_name" is: "score"."
            """,
            "max_turns":2,
            "summary_method":"last_msg"
        }
])

    return result

# DO NOT modify this code below.
if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please ensure you include a query for some restaurant when executing main."
    main(sys.argv[1])