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

def stream_launcher(tweet_listener, detail='text'):
        
    """
    Launches a tweet stream listener and filters tweets based on level of detail.
    
    Args:
    tweet_listener (tweepy.StreamingClient): A tweepy stream listener object.
    detail (str): Level of detail for tweet data to collect. 
                  Possible values: 'text', 'all' (default: 'text')
    
    Returns:
    None
    """
        
    if detail == 'text':
        tweet_listener.filter(
            tweet_fields="text"
        )

    elif detail == 'all':
        tweet_listener.filter(
        expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
        tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
        poll_fields="duration_minutes,end_datetime,id,options,voting_status",
        place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
        user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
        )