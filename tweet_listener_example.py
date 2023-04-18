# TWEET LISTENER EXAMPLE - FILTERED STREAM

import tweepy
import configparser
import json
from datetime import datetime
import modules.auth_module as auth_module
import modules.rule_handler as rule_handler
import modules.data_writer as data_writer

d0 = datetime.now()

# HYPERPARAMETERS
rate_limit = True
launch = True    # True if you want to start collecting tweets


# AUTHENTICATION
auth = auth_module.get_auth(config_file="config/config_FO.ini", auth_method="OAuth2")
api = auth[0]
auth_keys = auth[1]


# TWEET LISTENER

# build the tweet listener
class TweetListenerISTAT_V2(tweepy.StreamingClient):

    def on_connect(self):                       # check if the listener is connected
        print("Listener Connected")
    
    def on_tweet(self, tweet):                    # store the data in a .json file
        print(tweet)
    
    def on_error(self, tweet_code):             # handle errors
        if tweet_code == 420:
            return False        

listener = TweetListenerISTAT_V2(bearer_token = auth_keys['BEARER_TOKEN'], 
                                 wait_on_rate_limit = rate_limit)

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


# RULES

keywords = ("famiglia OR denaro")

# delete pre-existing rules
listener = rule_handler.clean_rules(listener)

# extract the list of rules
rule_list_istat = rule_handler.query_builder(keywords=keywords, 
                                             max_length=512, lang='it')
#rule_list_fiducia = rule_handler.query_builder(keywords=keywords_filter_fiducia,
#                                               max_length=512, lang='it')

# add the rules to the filtered stream
listener = rule_handler.push_rules(tweet_listener=listener, rules=rule_list_istat,
                                   rule_tag="filtro_istat", clean_push=False)

#listener = rule_handler.push_rules(tweet_listener=listener, rules=rule_list_fiducia,
#                                   rule_tag="filtro_fiducia", clean_push=False)


# launch the listener and choose what to store
if launch == True:
    listener.filter(
    expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
    tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
    poll_fields="duration_minutes,end_datetime,id,options,voting_status",
    place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
    user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
    media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
    )