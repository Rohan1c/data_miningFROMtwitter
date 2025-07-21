import os
import tweepy
from dotenv import load_dotenv
from collections import Counter
import matplotlib.pyplot as plt
import time
import datetime

load_dotenv()   # Load bearer token
bearer_token = os.getenv("BEARER_TOKEN")

if not bearer_token:
    raise Exception("Bearer token not loaded. Check your .env file.")

# Initializing the client
client = tweepy.Client(bearer_token=bearer_token)

# also intitializing the query
query = "football -is:retweet lang:en"

try:
    # Fetch tweets (LIMITED TO 10 AS WE R USING FREE TRIAL)
    tweets = client.search_recent_tweets(
        query=query,
        max_results=10,
        tweet_fields=["author_id"]
    )

    if not tweets.data:
        print("No tweets found.")
        exit()

    # Count tweets by user ID
    user_counter = Counter(tweet.author_id for tweet in tweets.data)

    # Fetch user details (like usernames)
    user_ids = list(user_counter.keys())
    users_response = client.get_users(ids=user_ids)

    # Map usernames to tweet counts
    usernames_dict = {user.username: user_counter[user.id] for user in users_response.data}

    # Print the dictionary
    print("Tweet counts by user:", usernames_dict)

    # Plotting the graph
    usernames = list(usernames_dict.keys())
    tweet_counts = list(usernames_dict.values())

    plt.figure(figsize=(10, 6))
    plt.bar(usernames, tweet_counts, color='skyblue')
    plt.xlabel("Usernames")
    plt.ylabel("Number of Tweets")
    plt.title("Most Active Users Tweeting about 'football'")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

except tweepy.TooManyRequests as e:
    reset_timestamp = int(e.response.headers.get("x-rate-limit-reset", 0))
    reset_time = datetime.datetime.fromtimestamp(reset_timestamp)
    now = datetime.datetime.now()
    wait_time = (reset_time - now).total_seconds()     #calculating the exact waiting period
    print(f"\nRate limit hit. Waiting until {reset_time.strftime('%H:%M:%S')} ({int(wait_time)} seconds)")
    time.sleep(max(wait_time, 0) + 1)
    print("Rate limit hit. Please wait and try again later.")

except Exception as e:
    print("Error:", e)
