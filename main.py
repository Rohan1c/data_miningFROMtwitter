import os
import tweepy
from dotenv import load_dotenv
import time
import datetime
from collections import Counter

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

if not bearer_token:
    raise Exception("Bearer token not loaded. Check your .env file.")

client = tweepy.Client(bearer_token=bearer_token)
query = "football -is:retweet lang:en"


while True:
    try:
        tweets = client.search_recent_tweets(query=query, max_results=10,tweet_fields=["author_id"])
        user_counter = Counter()
        for tweet in tweets.data:
            user_counter[tweet.author_id] += 1

        # Fetch usernames for those user IDs
        usernames_dict = {}
        user_ids = list(user_counter.keys())
        users_response = client.get_users(ids=user_ids)

        for user in users_response.data:
            usernames_dict[user.username] = user_counter[user.id]

        # Print the dictionary
        print(usernames_dict)

    except tweepy.TooManyRequests as e:
        reset_timestamp = int(e.response.headers.get("x-rate-limit-reset", 0))
        reset_time = datetime.datetime.fromtimestamp(reset_timestamp)
        now = datetime.datetime.now()
        wait_time = (reset_time - now).total_seconds()     #calculating the exact waiting period

        print(f"\nRate limit hit. Waiting until {reset_time.strftime('%H:%M:%S')} ({int(wait_time)} seconds)")
        time.sleep(max(wait_time, 0) + 1)  

    except Exception as e:
        print("Something else went wrong:", e)
        break
