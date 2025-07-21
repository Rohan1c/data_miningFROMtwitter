import os
import tweepy
from dotenv import load_dotenv
from collections import Counter
import matplotlib.pyplot as plt
import time
import datetime

# Load bearer token
load_dotenv()
bearer_token = os.getenv("BEARER_TOKEN")

if not bearer_token:
    raise Exception("Bearer token not loaded. Check your .env file.")

# Initialize Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

# Define your search query
query = "football -is:retweet lang:en"

try:
    # Fetch tweets (LIMITED TO 10 TO BE SAFE)
    tweets = client.search_recent_tweets(
        query=query,
        max_results=10,
        tweet_fields=["author_id"]
    )

    if not tweets.data:
        print("No tweets found.")
        exit()

    # Count tweets by author ID
    user_counter = Counter(tweet.author_id for tweet in tweets.data)

    # Fetch user details (usernames)
    user_ids = list(user_counter.keys())
    users_response = client.get_users(ids=user_ids)

    # Map usernames to tweet counts
    usernames_dict = {user.username: user_counter[user.id] for user in users_response.data}

    # Print dictionary
    print("Tweet counts by user:", usernames_dict)

    # Plot the graph
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
