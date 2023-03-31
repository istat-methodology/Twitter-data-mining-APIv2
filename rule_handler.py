# RULE HANDLER - WORK IN PROGRESS!!!

import tweepy

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


def query_builder(keywords, language=None, query=None, api="elevated"):

    """
    Builds a query string based on the provided keywords, language, and query parameters.

    Args:
        keywords (list of str): List of keywords to be included in the query.
        language (str, optional): Language to be included in the query. Defaults to None.
        query (str, optional): Additional query parameter to be included in the query. Defaults to None.
        api (str, optional): API to be used for the query. Defaults to 'elevated'.

    Returns:
        list of str: List of query strings to be used in the search.
    """
    lang_string = f" lang:{language}" if language else ""
    query_string = f" {query}" if query else ""
    
    len_query = len(lang_string + query_string)
    len_query += 2 if len_query > 0 else 0

    api_options = {
        'essential': (512 - len_query, 5),
        'elevated': (512 - len_query, 25),
        'academic': (1024 - len_query, 1000)
    }
    max_chars, max_rules = api_options.get(api, None)
    if max_chars is None:
        raise ValueError("\nERROR: 'api' must be either 'essential', 'elevated' or 'academic'.")

    # Create a single string from the list
    single_string = " OR ".join(keywords)
    # Split the single string into multiple strings based on the maximum length
    split_strings = []
    n_rules = 0
    start = 0
    while start < len(single_string):
        n_rules += 1
        # Find the end of the substring based on the maximum length
        end = start + max_chars
        # If the substring ends in the middle of a word, adjust the end to the end of the previous word
        end = single_string.rfind(" ", start, end+1)
        if end == -1:
            end = start + max_chars
        # If the substring ends in "OR", adjust the end to exclude it
        if single_string.endswith(" OR", start, end):
            end -= 3
        # If the substring starts with "OR", adjust the start to exclude it
        if single_string.startswith("OR ", start, end):
            start += 3
        query_i = f"({single_string[start:end]}){lang_string}{query_string}"
        # If the final string ends with a blank space, adjust the end to remove it
        query_i = query_i.rstrip()
        split_strings.append(query_i)
        start = end + 1
    
    if n_rules > max_rules:
        print(f"""\nWARNING: the number of rules ({n_rules}) exceeds the maximum number of rules ({max_rules}) 
        allowed by your API ({api}).""")
    else:
        print(f"\nthe final number of rules is {n_rules}.")

    split_strings_final = [keyword.replace("|", " ") for keyword in split_strings]

    return split_strings_final

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


def rule_handler(tweet_listener, keywords, api_tier='elevated', language='it', query='', clean_rules=True):

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
                                                                language=language,
                                                                query=query)
        listener = rule_handler.push_rules(tweet_listener=listener,
                                           rule = query_list[f'{rule}_rule'],
                                           rule_tag=rule,
                                           clean_push=False)
    
    return listener