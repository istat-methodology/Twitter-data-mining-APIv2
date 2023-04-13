# TWEET SEARCH EARLY EXAMPLE

import tweepy
import json
import datetime
import modules.auth_module as auth_module
import modules.rule_handler as rule_handler

#keyword_filter = "FiltroFiducia.txt"
rate_limit = True

# authentication
auth = auth_module.get_auth("config/config.ini")
client = tweepy.Client(bearer_token = auth['BEARER_TOKEN'], 
                       consumer_key = auth['API_KEY'], 
                       consumer_secret = auth['API_KEY_SECRET'], 
                       access_token = auth['ACCESS_TOKEN'],
                       access_token_secret = auth['ACCESS_TOKEN_SECRET'],
                       return_type=dict, 
                       wait_on_rate_limit=rate_limit)

# FILTERS

# import and pre-process the filter
keywords_filter_istat_raw = open(f"filters/FiltroIstat.txt", "r").readlines()
keywords_filter_istat_nospace = [keyword.replace(" ", "|") for keyword in keywords_filter_istat_raw]
keywords_filter_istat = [word.strip() for word in keywords_filter_istat_nospace]

keywords_filter_fiducia_raw = open(f"filters/FiltroFiducia.txt", "r").readlines()
keywords_filter_fiducia_nospace = [keyword.replace(" ", "|") for keyword in keywords_filter_fiducia_raw]
keywords_filter_fiducia = [word.strip() for word in keywords_filter_fiducia_nospace]

# remove words in filter istat that are present in filter fiducia
# check if one list is a perfect subset of the other, otherwise create a third list
keywords_filter_istat_unique = [word for word in keywords_filter_istat if word not in keywords_filter_fiducia]
keywords_filter_fiducia_unique = [word for word in keywords_filter_fiducia if word not in keywords_filter_istat]

# build query
rule_list_istat = rule_handler.query_builder(keywords=keywords_filter_istat_unique, 
                                             api='elevated', language='it', query='')
rule_list_fiducia = rule_handler.query_builder(keywords=keywords_filter_fiducia,
                                               api='elevated', language='it', query='')

start_date = datetime.datetime(2023, 4, 11, 23, 00, 00)
end_date = datetime.datetime(2023, 4, 13, 11, 00, 00)

for query in rule_list_istat:
        tweets_filtroistat = tweepy.Paginator(client.search_recent_tweets, query=f"({query})",
                                              start_time = start_date, end_time = end_date,
                                              expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                                              tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
                                              poll_fields="duration_minutes,end_datetime,id,options,voting_status",
                                              place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
                                              user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                                              media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
                                              max_results=100).flatten(limit=1000000)
        with open(f'data/output/search_data/tweets_filtroistat_batch_{start_date}_{end_date}.json', 'a') as tf:
                tf.write('\n')
                json.dump(tweets_filtroistat, tf)

for query in rule_list_fiducia:
        tweets_filtrofiducia = tweepy.Paginator(client.search_recent_tweets, query=f"({query})",
                                                start_time = start_date, end_time = end_date,
                                                expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                                                tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
                                                poll_fields="duration_minutes,end_datetime,id,options,voting_status",
                                                place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
                                                user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                                                media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
                                                max_results=100).flatten(limit=1000000)
        with open(f'data/output/search_data/tweets_filtrofiducia_batch_{start_date}_{end_date}.json', 'a') as tf:
                tf.write('\n')
                json.dump(tweets_filtrofiducia, tf)
        

#tweets1 = tweepy.Paginator(client.search_recent_tweets, query=f"({keywords_single_string_1}) lang:it",
#                           start_time = start_date, end_time = end_date,
#                           expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
#                           tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
#                           poll_fields="duration_minutes,end_datetime,id,options,voting_status",
#                           place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
#                           user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
#                           media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
#                           max_results=100).flatten(limit=1000000)

#tweets2 = tweepy.Paginator(client.search_recent_tweets, query=f"({keywords_single_string_2}) lang:it",
#                           start_time = start_date, end_time = end_date,
#                           expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
#                           tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
#                           poll_fields="duration_minutes,end_datetime,id,options,voting_status",
#                           place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
#                           user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
#                           media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width", 
#                           max_results=100).flatten(limit=1000000)

#tweets1_lst = []
#for tweet in tweets1:
#    tweets1_lst.append(tweet)
#    print(len(tweets1_lst))

#with open(f'data/output/search_data/tweets5.json', 'w') as tf:
#            tf.write('\n')
#            json.dump(tweets1_lst, tf)

#tweets2_lst = []
#for tweet in tweets2:
#    tweets2_lst.append(tweet)
#    print(len(tweets1_lst)+len(tweets2_lst))

#with open(f'data/output/search_data/tweets6.json', 'w') as tf:
#            tf.write('\n')
#            json.dump(tweets2_lst, tf)