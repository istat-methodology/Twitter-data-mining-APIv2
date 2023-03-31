import tweepy
import data_writer
import json
from datetime import datetime

def stream_builder(bearer_token, display_text=False, store_data=False, data_path='output/listener_data', wait_on_rate_limit=True):
    """
    Create and return a Twitter stream listener that can display or store incoming tweets.

    Parameters:
    - bearer_token (str): The bearer token for authenticating with the Twitter API.
    - display_text (bool): Whether to print the full text of incoming tweets to the console. Default: False.
    - store_data (bool): Whether to store incoming tweets in a JSON file. Default: False.
    - data_path (str): The path to the directory where the JSON files should be stored. Default: 'output/listener_data'.
    - wait_on_rate_limit (bool): Whether to wait when the Twitter API rate limit is exceeded. Default: True.

    Returns:
    - A MyStreamingClient instance that can be used to connect to the Twitter stream and receive incoming tweets.
    """

    class MyStreamingClient(tweepy.StreamingClient):

        def on_connect(self):
            print("Listener connected")
            self.tweet_count = 0
            self.d0 = datetime.now()

        def on_data(self, data):
            if display_text:
                print(data.text)
            self.tweet_count += 1
            if store_data:
                jsonData=json.loads(data)
                data_writer.write_tweets_to_json(data=jsonData,
                                                 d0=self.d0,
                                                 path=data_path,
                                                 format_string="{prefix}.{now.year}{now.month:02d}{now.day:02d}-{now.hour:02d}.{suffix}.json")

        def on_error(self, tweet_code):
            if tweet_code == 420:
                print("Rate limit exceeded. Disconnecting the stream...")
                return False

    listener = MyStreamingClient(bearer_token=bearer_token, 
                                 wait_on_rate_limit=wait_on_rate_limit)
    
    return listener