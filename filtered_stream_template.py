# Filtered Stream template - Work in progress

import tweepy
import data_writer
import json
import authentication
import rule_handler
import stream_builder
from datetime import datetime

api_tier = 'elevated'
launch_stream = False

# Enter your API keys and access tokens
auth = authentication.get_auth(config_file="auth/config.ini", auth_method="OAuth2")
api = auth[0]
auth_keys = auth[1]

# Set up the filtered stream
listener = stream_builder.stream_builder(bearer_token=auth_keys['BEARER_TOKEN'],
                                         display_text=True,
                                         store_data=False,
                                         wait_on_rate_limit=True)

# Define the filter rules
keyword_list_1 = ['put', 'your keywords', 'here']
keyword_list_2 = ['put', 'other keywords', 'here']
rules = [keyword_list_1, keyword_list_2]

listener = rule_handler.rule_handler(tweet_listener=listener, 
                                     keywords=rules, 
                                     api_tier=api_tier, 
                                     language='it', 
                                     query='')

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