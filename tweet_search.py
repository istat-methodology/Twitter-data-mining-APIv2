import tweepy
import json
import datetime
import authentication

keyword_filter = "FiltroFiducia.txt"
rate_limit = True

# authentication
auth = authentication.get_auth("auth/config.ini")
client = tweepy.Client(bearer_token = auth['BEARER_TOKEN'], 
                       consumer_key = auth['API_KEY'], 
                       consumer_secret = auth['API_KEY_SECRET'], 
                       access_token = auth['ACCESS_TOKEN'],
                       access_token_secret = auth['ACCESS_TOKEN_SECRET'],
                       return_type=dict, 
                       wait_on_rate_limit=rate_limit)

# filter
keywords = open(f"filters/{keyword_filter}", "r").readlines()
keywords_1 = [word.strip() for word in keywords[0:29]]
keywords_single_string_1 = ' OR '.join(keywords_1)
keywords_2 = [word.strip() for word in keywords[30:59]]
keywords_single_string_2 = ' OR '.join(keywords_2)

start_date = datetime.datetime(2023, 3, 18, 00, 00, 00)
end_date = datetime.datetime(2023, 3, 20, 12, 00, 00)

tweets1 = tweepy.Paginator(client.search_recent_tweets, query=f"({keywords_single_string_1}) lang:it",
                           start_time = start_date, end_time = end_date,
                           expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                           tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
                           poll_fields="duration_minutes,end_datetime,id,options,voting_status",
                           place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
                           user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                           media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
                           max_results=100).flatten(limit=1000000)

tweets2 = tweepy.Paginator(client.search_recent_tweets, query=f"({keywords_single_string_2}) lang:it",
                           start_time = start_date, end_time = end_date,
                           expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                           tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
                           poll_fields="duration_minutes,end_datetime,id,options,voting_status",
                           place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
                           user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                           media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
                           max_results=100).flatten(limit=1000000)

tweets1_lst = []
for tweet in tweets1:
    tweets1_lst.append(tweet)
    print(len(tweets1_lst))

with open(f'tweets5.json', 'w') as tf:
            tf.write('\n')
            json.dump(tweets1_lst, tf)

tweets2_lst = []
for tweet in tweets2:
    tweets2_lst.append(tweet)
    print(len(tweets1_lst)+len(tweets2_lst))

with open(f'tweets6.json', 'w') as tf:
            tf.write('\n')
            json.dump(tweets2_lst, tf)