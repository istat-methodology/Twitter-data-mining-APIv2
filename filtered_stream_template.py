# Filtered Stream template - Work in progress

import tweepy
import data_writer
import json
import authentication
import rule_handler
from datetime import datetime

d0 = datetime.now()
wait_on_rate_limit = True
launch_stream = False

# Enter your API keys and access tokens
auth = authentication.get_auth(config_file="auth/config.ini", auth_method="OAuth2")
api = auth[0]
auth_keys = auth[1]

# Create a stream listener
class MyStreamListener(tweepy.StreamingClient):

    def on_connect(self):                       
        print("Listener Connected")
    
    def on_data(self, data):
        # Define what to do when a new tweet is received
        jsonData = json.loads(data)
        data_writer.write_tweets_to_json(data=jsonData,
                                         d0=d0,
                                         format_string="{prefix}.{now.year}{now.month:02d}{now.day:02d}-{now.hour:02d}.{suffix}.json")        
        
    def on_error(self, status_code):
        # Define what to do when an error occurs
        if status_code == 420:
            print("Rate limit exceeded. Disconnecting the stream...")
            return False

# Set up a filtered stream
listener = MyStreamListener(bearer_token = auth_keys['BEARER_TOKEN'], 
                            wait_on_rate_limit = wait_on_rate_limit)

# Define the filter rules
keyword_list_1 = ['put', 'your keywords', 'here']
keyword_list_2 = ['put', 'other keywords', 'here']
rules = [keyword_list_1, keyword_list_2]

listener = rule_handler.clean_rules(listener)
rule_list_1 = rule_handler.query_builder(keywords=keyword_list_1, api='elevated', 
                                         language='en', query='')
rule_list_2 = rule_handler.query_builder(keywords=keyword_list_2, api='elevated', 
                                         language='en', query='')
listener = rule_handler.push_rules(tweet_listener=listener, rules=rule_list_1,
                                   rule_tag="keywords_1", clean_push=False)

listener = rule_handler.push_rules(tweet_listener=listener, rules=rule_list_2,
                                   rule_tag="keywords_2", clean_push=False)

# Set up the stream rules
# launch the listener and choose what to store
if launch_stream == True:
    listener.filter(
    expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
    tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
    poll_fields="duration_minutes,end_datetime,id,options,voting_status",
    place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
    user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
    media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
    )