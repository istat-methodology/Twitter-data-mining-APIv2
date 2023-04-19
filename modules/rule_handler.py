# RULE HANDLER - WORK IN PROGRESS!!!

import tweepy
from typing import List

# clean_rules: this function deletes all the rules from the filtered stream passed as an argument
def clean_rules(tweet_listener):

    """
    Deletes all the pre-existing rules applied to the filtered stream.

    Args:
        tweet_listener (variable): The filtered stream object.
    
    Returns:
        variable: Clean filtered stream object.
    """
    
    result = tweet_listener.get_rules()

    if result.data is not None:
        rule_ids = [rule for rule in result.data]
        print(f"\nrule(s) marked to delete: {rule_ids}")
        tweet_listener.delete_rules(rule_ids)
    else:
        print("\nno rules to delete.")
    
    return tweet_listener


def query_builder(keywords: List[str], lang: str = 'it', api_tier: str = 'elevated') -> List[str]:

    """
    Create a list of Twitter API search queries from a list of keywords.

    Args:
        keywords (List[str]): A list of keywords to be used in the search queries.
        lang (str): A string representing the language of the search queries.
        max_length (int): An integer representing the maximume number of character for each query. 
        Defaults to 512.

    Returns:
        List[str]: A list of Twitter API search queries.
    """
    if api_tier == 'essential' or 'elevated':
        max_length = 512
    elif api_tier == 'academic':
        max_length = 1024

    queries = []
    current_query = '('
    for keyword in keywords:
        if len(current_query + keyword + f' lang{lang}') < max_length:
            current_query += keyword + ' OR '
        else:
            queries.append(current_query[:-4] + f') lang:{lang}')
            current_query = '(' + keyword + ' OR '
    queries.append(current_query[:-4] + f') lang:{lang}')

    return queries

# push_rules: this function automatically adds a list of rules to the stream
def push_rules(tweet_listener, rules, rule_tag=None, clean_push=False):

    """
    Adds a list of rules to the filtered stream.

    Args:
        tweet_listener (variable): The filtered stream object to add the rules to.
        rules (list of str): List of rules to be applied to the filtered stream.
        rule_tag (str, optional): Tag of the set of rules. Defaults to None.
        clean_push (bool, optional): If True, clean rules before adding new ones. Defaults to False.
    
    Returns:
        variable: Filtered stream object.
    """

    if clean_push == True:
        clean_rules(tweet_listener)

    rules = []

    for i in range(0, len(rules)):
        rule_i = tweepy.StreamRule(rules[i], tag=rule_tag)
        rules.append(rule_i)
    
    tweet_listener.add_rules(rules)

    return tweet_listener


def rule_handler(tweet_listener, keywords, api_tier='elevated', lang='it', clean_rules=True):

    """
    Update the rules for a Twitter stream listener based on a set of keywords.

    Parameters:
    - tweet_listener: An instance of tweepy.StreamingClient or one of its subclasses, representing the listener to which the rules should be applied.
    - keywords (list of str): A set or list of strings representing the keywords to use for the rules.
    - api_tier (str): A string representing the Twitter API tier to use for the rules. Default: 'elevated'.
    - language (str): A string representing the language of the tweets to be captured by the rules. Default: 'it'.
    - query (str): A string representing additional filters to apply to the rules. Default: ''.
    - clean_rules (bool): Whether to delete pre-existing rules before adding the new ones. Defaults to True.

    Returns:
    - A tweepy.StreamingClient or one of its subclasses, representing the updated listener with the new rules in place.
    """
    if clean_rules == True:
        listener = rule_handler.clean_rules(tweet_listener)

    query_list = []

    for rule in list(keywords):
        query_list[f'{rule}_rule'] = rule_handler.query_builder(keywords=rule,
                                                                api=api_tier,
                                                                lang=lang)
        
        listener = rule_handler.push_rules(tweet_listener=listener,
                                           rule = query_list[f'{rule}_rule'],
                                           rule_tag=rule,
                                           clean_push=False)
    
    return listener