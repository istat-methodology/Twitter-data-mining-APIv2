# RULE HANDLER - WORK IN PROGRESS!!!

import tweepy

# clean_rules: this function deletes all the rules from the filtered stream passed as an argument
def clean_rules(tweet_listener):
    
    result = tweet_listener.get_rules()

    if result.data != None:
        rule_ids = [rule for rule in result.data]
        print(f"\nrule(s) marked to delete: {rule_ids}")
        tweet_listener.delete_rules(rule_ids)
    else:
        print("\nno rules to delete.")
    
    return tweet_listener

# query_builder: this function automatically builds Twitter API v2 queries based on keywords
def query_builder(keywords, language, query, api):

    if language != None:
        lang_string = f" lang:{language}"
        len_lang_string = len(lang_string)
    
    if query != None:
        query_string = f" {query}"
        len_query_string = len(query_string)
    else:
        query_string = None
        len_query_string = 0
    
    if (len_lang_string + len_query_string) > 0:
        len_query = (len_lang_string + len_query_string) - 2 # -2 accounts for the parentheses
    else:
        len_query = 0

    if api == 'essential':
        max_chars = 512 - len_query
        max_rules = 5
    elif api == 'elevated':
        max_chars = 512 - len_query
        max_rules = 25
    elif api == 'academic':
        max_chars = 1024 - len_query
        max_rules = 1000
    else:
        print("\nERROR: 'api' must be 'essential', 'elevated' or 'academic'.")

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
        print(f"""WARNING: the number of rules ({n_rules}) exceeds the maximum number of rules ({max_rules}) 
        allowed by your API ({api}).""")
    else:
        print(f"\nthe final number of rules is {n_rules}.\n")

    split_strings_final = [keyword.replace("|", " ") for keyword in split_strings]

    return split_strings_final
