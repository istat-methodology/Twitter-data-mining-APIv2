import tweepy
import json
import os
from datetime import datetime
import pandas as pd
from modules.query_handler import QueryHandler

api_tier          : str      = "elevated"
bearer_token      : str      = "your bearer token"
wordlist_path     : str      = "filters"
wait_on_rate_limit: bool     = True
store_data        : bool     = True
start_time        : datetime = datetime(2023, 4, 11, 23, 0, 0, 0)
end_time          : datetime = datetime(2023, 4, 13, 11, 0, 0, 0)


client = tweepy.Client(bearer_token)

if store_data is True:
    path = os.getcwd()  
    data_folder_path = os.path.join(path, "data")

    if not os.path.exists(data_folder_path):
        os.mkdir(data_folder_path)

# import filters
keywords_filter_istat_raw = open(f"filters/FiltroIstat.txt", "r").readlines()
keywords_filter_istat = [word.strip() for word in keywords_filter_istat_raw]

keywords_filter_fiducia_raw = open(f"filters/FiltroFiducia.txt", "r").readlines()
keywords_filter_fiducia = [word.strip() for word in keywords_filter_fiducia_raw]

keywords_filter_istat_unique = [word for word in keywords_filter_istat if word not in keywords_filter_fiducia]

# build queries
query_filtroistat = QueryHandler.query_builder(keywords=keywords_filter_istat_unique, lang='it')
query_filtrofiducia = QueryHandler.query_builder(keywords=keywords_filter_fiducia, lang='it')

# Paginator
for query in query_filtrofiducia:        
    tweets_fiducia = tweepy.Paginator(client.search_recent_tweets, query=f'{query}',
                                      start_time=start_time, end_time=end_time,
                                      expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                                      tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
                                      poll_fields="duration_minutes,end_datetime,id,options,voting_status",
                                      place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
                                      user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                                      media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
                                      max_results=100).flatten(limit=10000000)
        
    
    file_name = f"TweetsRawData_backup_filtrofiducia.json"
    with open(f"{file_name}", 'a') as tf:
        for tweet in tweets_fiducia:
            tf.write('\n')
            json.dump(tweet, tf)

for query in query_filtroistat:        
    tweets_istat = tweepy.Paginator(client.search_recent_tweets, query=f'{query}',
                                    start_time=start_time, end_time=end_time,
                                    expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                                    tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
                                    poll_fields="duration_minutes,end_datetime,id,options,voting_status",
                                    place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
                                    user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                                    media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
                                    max_results=100).flatten(limit=10000000)
        
    
    file_name = f"TweetsRawData_backup_filtroistat.json"
    with open(f"{file_name}", 'a') as tf:
        for tweet in tweets_fiducia:
            tf.write('\n')
            json.dump(tweet, tf)