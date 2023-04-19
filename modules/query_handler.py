import tweepy
from typing import List

class QueryHandler:
    def __init__(self, tweet_listener, api_tier: str = "elevated"):
        self.tweet_listener = tweet_listener
        if api_tier == "essential":
            self.max_query_length = 512
        if api_tier == "elevated":
            self.max_query_length = 512
        elif api_tier == "academic":
            self.max_query_length = 1024 

    def clean_rules(self):
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
    
    def push_rules(self, rules: List[str], rule_tag: str = None, clean_push: bool = False):
        if clean_push is True:
            self.clean_rules()
        
        stream_rules =[]
        for rule in rules:
            stream_rule = tweepy.StreamRule(rule, tag=rule_tag)
            stream_rules.append(stream_rule)
        
        self.tweet_listener.add_rules(stream_rules)

        return self.tweet_listener