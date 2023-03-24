# Tweet listener built with tweepy for Twitter API V2

import tweepy
import configparser
import json
from datetime import datetime
import authentication

dt_0 = datetime.now()

# hyperparameters
keyword_filter = "FiltroFiducia.txt"
rate_limit = True

# authentication
auth = authentication.get_auth("auth/config.ini")
api = auth['api']

# define the tweet listener
class TweetListenerISTAT_V2(tweepy.StreamingClient):
    # check if the listener is connected
    def on_connect(self):
        print("Listener Connected")
    # store the data in a .json file
    def on_data(self, data):
        jsonData = json.loads(data)
        #print(jsonData)
        # save the -json file to directory ----- METTERE MESE A DOPPIA CIFRA
        dt_1 = datetime.now()
        with open(f'data/TweetsRawData.{dt_1.year}{dt_1.month}{dt_1.day}-{dt_1.hour}.{keyword_filter}{dt_0.year}{dt_0.month}{dt_0.day}-{dt_0.hour}.queue.json', 'a') as tf:
            tf.write('\n')
            json.dump(jsonData, tf)
        return True
    # handle errors
    def on_error(self, tweet_code):
        if tweet_code == 420:
            return False        

listener = TweetListenerISTAT_V2(auth['BEARER_TOKEN'], wait_on_rate_limit=rate_limit)

# clean-up pre-existing rules
rule_ids = []
result = listener.get_rules()

if result.data != None:
    for rule in result.data:
        print(f"rule marked to delete: {rule.id} - {rule.value}")
        rule_ids.append(rule.id)

        listener.delete_rules(rule_ids)
        listener = TweetListenerISTAT_V2(auth['BEARER_TOKEN'], wait_on_rate_limit=rate_limit)
else:
    print("no rules to delete")

# import the keyword filter
keywords = open(f"filters/{keyword_filter}", "r").readlines()
keywords_1 = [word.strip() for word in keywords[0:29]]
keywords_single_string_1 = ' OR '.join(keywords_1)
keywords_2 = [word.strip() for word in keywords[30:59]]
keywords_single_string_2 = ' OR '.join(keywords_2)

# add new rules
rule_1 = tweepy.StreamRule(f"({keywords_single_string_1}) lang:it", tag="rule 1")
rule_2 = tweepy.StreamRule(f"({keywords_single_string_2}) lang:it", tag="rule 2")
rules = [rule_1, rule_2]

listener.add_rules(rules)

# launch the listener and choose what to store
listener.filter(
expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
poll_fields="duration_minutes,end_datetime,id,options,voting_status",
place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
)