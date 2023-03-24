# TWEET LISTENER - WORK IN PROGRESS!!!

import tweepy
import configparser
import json
from datetime import datetime
import authentication
import rule_handler

d0 = datetime.now()

# hyperparameters
keyword_filter = "FiltroFiducia.txt"
rate_limit = True
path_data = "output/listener_data"

# authentication
auth = authentication.get_auth("auth/config.ini")

# build the tweet listener
class TweetListenerISTAT_V2(tweepy.StreamingClient):

    def on_connect(self):                       # check if the listener is connected
        print("Listener Connected")
    
    def on_data(self, data):                    # store the data in a .json file
        jsonData = json.loads(data)
        d1 = datetime.now()
        file_name = f"TweetsRawData.{d1.year}{d1.month:02d}{d1.day:02d}-{d1.hour:02d}.{keyword_filter}{d0.year}{d0.month:02d}{d0.day:02d}-{d0.hour:02d}.queue.json"
        with open(f"data/{file_name}", 'a') as tf:
            tf.write('\n')
            json.dump(jsonData, tf)
        return True
    
    def on_error(self, tweet_code):             # handle errors
        if tweet_code == 420:
            return False        

listener = TweetListenerISTAT_V2(bearer_token = auth['BEARER_TOKEN'], 
                                 wait_on_rate_limit = rate_limit)

# rules
listener = rule_handler.clean_rules(listener)
rule_handler.add_rules(keywords="FiltroIstat.txt", api="elevated")
