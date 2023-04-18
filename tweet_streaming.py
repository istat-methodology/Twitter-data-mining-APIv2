import tweepy
import json
import os
import requests
import logging
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem
from dapr.clients.grpc._request import TransactionalStateOperation, TransactionOperationType
from typing import List

consumer_key      : str  = os.getenv("CONSUMER_KEY")
consumer_secret   : str  = os.getenv("CONSUMER_SECRET")
api_tier          : str  = os.getenv("API_TIER", "elevated")
bearer_token      : str  = os.getenv("BEARER_TOKEN")
wordlist_path     : str  = os.getenv("WORDLIST_PATH", ".")
wait_on_rate_limit: bool = True

DAPR_STORE_NAME = "statekeep"
PUBSUB_NAME     = "ehpubsub"
TOPIC_NAME      = "tweetsstream"

client = tweepy.Client(bearer_token)

class TweetListener(tweepy.StreamingClient):
    def on_connect(self):
        print("Listener connected succesfully.")
    
    def on_data(self, tweet_raw):
        with DaprClient() as client:
            currentNum = client.get_state(DAPR_STORE_NAME, "tweetNum")
            client.save_state(DAPR_STORE_NAME, "tweetNum", currentNum + 1) 

            result = client.publish_event(
                pubsub_name=PUBSUB_NAME,
                topic_name=TOPIC_NAME,
                data=json.dumps(tweet_raw),
                data_content_type='application/json',
            )
    
    def on_errors(self, status_code: int) -> bool:
        if status_code==400:
            return False

class QueryHandler:
    def init(self, tweet_listener, api_tier: str = "elevated"):
        self.tweet_listener = tweet_listener
        if api_tier == "essential":
            self.max_query_length = 512
        if api_tier == "elevated":
            self.max_query_length = 512
        elif api_tier == "academic":
            self.max_query_length = 1024 

    def clean_rules(self) -> TweetListener:
        result = self.tweet_listener.get_rules()

        if result.data is not None:
            rule_ids = [rule.id for rule in result.data]
            print(f"rule(s) marked to delete: {rule_ids}")

            self.tweet_listener.delete_rules(rule_ids)
        else:
            print("no rules marked to delete")

        return self.tweet_listener
    
    def query_builder(self, keywords: List[str], sep: str = "OR", lang: str = "it") -> List[str]:
        queries = []
        current_query = "("

        for keyword in keywords:
            if len(current_query + keyword + f" lang:{lang}") < self.max_query_length:
                current_query += keyword + f" {sep} "
            else:
                queries.append(current_query[:-(len(sep)+2)]+ f') lang:{lang}')
                current_query = "(" + keyword + f" {sep} "
        queries.append(current_query[:-(len(sep)+2)] + f") lang:{lang}")

        return queries
    
    def push_rules(self, rules: List[str], rule_tag: str = None, clean_push: bool = False) -> TweetListener:
        if clean_push is True:
            self.clean_rules()
        
        stream_rules =[]
        for rule in rules:
            stream_rule = tweepy.StreamRule(rule, tag=rule_tag)
            stream_rules.append(stream_rule)
        
        self.tweet_listener.add_rules(stream_rules)

        return self.tweet_listener

# authentication
authenticator = TwitterAuthenticator(bearer_token)
api = authenticator.authenticate()

# tweet listener
listener = TweetListener(bearer_token=bearer_token, wait_on_rate_limit=wait_on_rate_limit)

# import keyword filters
keywords_filter_istat_raw = open(f"{wordlist_path}/filters/FiltroIstat.txt", "r").readlines()
keywords_filter_istat = [word.strip() for word in keywords_filter_istat_raw]

keywords_filter_fiducia_raw = open(f"{wordlist_path}/filters/FiltroFiducia.txt", "r").readlines()
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
if launch_stream == True:
    listener.filter(
        expansions="attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
        tweet_fields="attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld,edit_history_tweet_ids,edit_controls",
        poll_fields="duration_minutes,end_datetime,id,options,voting_status",
        place_fields="contained_within,country,country_code,full_name,geo,id,name,place_type",
        user_fields="created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        media_fields="duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
    )
