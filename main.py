import os
import tweepy
from dotenv import load_dotenv
import time
import datetime

load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

if not bearer_token:
    raise Exception("Bearer token not loaded. Check your .env file.")

client = tweepy.Client(bearer_token=bearer_token)
query = "football"

while True:
    try:
        tweets = client.search_recent_tweets(query=query, max_results=10)
        for tweet in tweets.data:
            print(tweet.text)
        break  # exit the loop if successful

    except tweepy.TooManyRequests as e:
        reset_timestamp = int(e.response.headers.get("x-rate-limit-reset", 0))
        reset_time = datetime.datetime.fromtimestamp(reset_timestamp)
        now = datetime.datetime.now()
        wait_time = (reset_time - now).total_seconds()

        print(f"\n❌ Rate limit hit. Waiting until {reset_time.strftime('%H:%M:%S')} ({int(wait_time)} seconds)")
        time.sleep(max(wait_time, 0) + 1)  # wait and retry

    except Exception as e:
        print("Something else went wrong:", e)
        break
