import tweepy
import json
import os
from typing import List
from datetime import datetime
from modules.query_handler import QueryHandler

api_tier          : str      = "elevated"
bearer_token      : str      = "your bearer token"
wordlist_path     : str      = "filters"
wait_on_rate_limit: bool     = True
launch_stream     : bool     = False
store_data        : bool     = True
stream_start_date : datetime = datetime.now()


client = tweepy.Client(bearer_token)

if store_data is True:
    path = os.getcwd()  
    data_folder_path = os.path.join(path, "data")

    if not os.path.exists(data_folder_path):
        os.mkdir(data_folder_path)

class TweetListener(tweepy.StreamingClient):
    def on_connect(self):
        print("Listener connected succesfully.")
        if store_data is True:
            os.mkdir('/data/tweet_streaming')
    
    def on_data(self, tweet_raw):
        if store_data is True:                    
            jsonData = json.loads(tweet_raw)
            current_date = datetime.now()
            file_name = f"TweetsRawData.{stream_start_date.year}{stream_start_date.month:02d}{stream_start_date.day:02d}-{current_date.hour:02d}.FiltroIstat{current_date.year}{current_date.month:02d}{current_date.day:02d}-{current_date.hour:02d}.queue.json"
            with open(f"data/{file_name}", 'a') as tf:
                tf.write('\n')
                json.dump(jsonData, tf)
            return True
    
    def on_errors(self, status_code: int) -> bool:
        if status_code==400:
            return False
        

# tweet listener
listener = TweetListener(bearer_token=bearer_token, wait_on_rate_limit=wait_on_rate_limit)

# import keyword filters
keywords_filter_istat_raw = open(f"{wordlist_path}/FiltroIstat.txt", "r").readlines()
keywords_filter_istat = [word.strip() for word in keywords_filter_istat_raw]

keywords_filter_fiducia_raw = open(f"{wordlist_path}/FiltroFiducia.txt", "r").readlines()
keywords_filter_fiducia = [word.strip() for word in keywords_filter_fiducia_raw]

keywords_filter_istat_unique = [word for word in keywords_filter_istat if word not in keywords_filter_fiducia]

# build search queries
query_handler = QueryHandler(listener, api_tier=api_tier)

query_filtroistat = query_handler.query_builder(keywords=keywords_filter_istat_unique)
query_filtrofiducia = query_handler.query_builder(keywords=keywords_filter_fiducia)

listener = query_handler.clean_rules()
listener = query_handler.push_rules(rules=query_filtrofiducia, rule_tag='filtrofiducia')
listener = query_handler.push_rules(rules=query_filtroistat, rule_tag='filtroistat')

# launch the listener and choose what to store
if launch_stream is True:
    listener.filter(
        expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
        tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
        poll_fields="duration_minutes,end_datetime,id,options,voting_status",
        place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
        user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
    )