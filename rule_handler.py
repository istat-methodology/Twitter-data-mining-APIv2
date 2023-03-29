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

    if result.data != None:
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

    if language is not None:
        lang_string = f" lang:{language}"
    else:
        lang_string = ""
    
    if query is not None:
        query_string = f" {query}"
    else:
        query_string = ""

    if (len(lang_string + query_string)) > 0:
        len_query = len(lang_string + query_string) + 2    # -2 accounts for the () brackets
    else:
        len_query = 0

    if api == 'essential':
        max_chars, max_rules = (512 - len_query), 5
    elif api == 'elevated':
        max_chars, max_rules = (512 - len_query), 25
    elif api == 'academic':
        max_chars, max_rules = (1024 - len_query), 1000
    else:
        raise ValueError("\nERROR: 'api' must be either 'essential', 'elevated' or 'academic'.")

    # Create a single string from the list
    single_string = " OR ".join(keywords)
    # Split the single string into multiple strings based on the maximum length
    split_strings = []
    n_rules = 0
    start = 0
    while start < len(single_string):
        n_rules = n_rules + 1
        # Find the end of the substring based on the maximum length
        end = start + max_chars
        if end < len(single_string):
            # If the substring ends in the middle of a word, adjust the end to the end of the previous word
            while single_string[end] != " ":
                end -= 1
        # If the substring ends in "OR", adjust the end to exclude it
        if single_string[end-2:end] == "OR":
            end -= 3
        # If the substring starts with "OR", adjust the start to exclude it
        if single_string[start:start+3] == "OR ":
            start += 3
        query_i = f"({single_string[start:end]}){lang_string}{query_string}"
        # If the final string ends with a blank space, adjust the end to remove it
        if query_i[-1] == " ":
            query_i_nospace = query_i[:-1]
            split_strings.append(query_i_nospace)
        else:
            split_strings.append(query_i)
        start = end + 1
    
    if n_rules > max_rules:
        print(f"""\nWARNING: the number of rules ({n_rules}) exceeds the maximum number of rules ({max_rules}) 
        allowed by your API ({api}).\n""")
    else:
        print(f"\nthe final number of rules is {n_rules}.\n")

    split_strings_final = [keyword.replace("|", " ") for keyword in split_strings]

    return split_strings_final

# push_rules: this function automatically adds a list of rules to the stream
def push_rules(tweet_listener, rules, rule_tag=None, clean_push=False):

    """
    Adds a list of rules to the filtered stream.

    Args:
        tweet_listener (variable): The filtered stream object to add the rules to.
        rules(list of str): List of rules to be applied to the filtered stream.
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