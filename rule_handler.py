# RULE HANDLER - WORK IN PROGRESS!!!

import tweepy

def clean_rules(tweet_listener):
    
    result = tweet_listener.get_rules()

    if result.data != None:
        rule_ids = [rule for rule in result.data]
        print(f"rule(s) marked to delete: {rule_ids}")
        tweet_listener.delete_rules(rule_ids)
    else:
        print("no rules to delete")
    
    return(tweet_listener)

def split_string_by_length(words_list, max_chars_per_string):
    words_string = ' '.join(words_list)
    result = []
    current_string = ''
    for word in words_string.split():
        if len(current_string) + len(word) + 1 <= max_chars_per_string:
            if current_string == '':
                current_string = word
            else:
                current_string = current_string + ' ' + word
        else:
            result.append(current_string)
            current_string = word
    result.append(current_string)
    return result

def add_rules(keywords, api):
    keyword_filter_raw = open(f"filters/{keywords}", "r").readlines()
    keyword_filter = [word.strip() for word in keyword_filter_raw]
    keyword_filter_string = ' OR '.join(keyword_filter)

    if api == 'essential':
        max_chars = 512
        max_rules = 5
    elif api == 'elevated':
        max_chars = 512
        max_rules = 25
    elif api == 'academic':
        max_chars = 1024
        max_rules = 1000
    else:
        print("ERROR: 'api' must be 'essential', 'elevated' or 'academic'.")

def split_string(keywords, api):

    if api == 'essential':
        max_chars = 512
        max_rules = 5
    elif api == 'elevated':
        max_chars = 512
        max_rules = 25
    elif api == 'academic':
        max_chars = 1024
        max_rules = 1000
    else:
        print("ERROR: 'api' must be 'essential', 'elevated' or 'academic'.")

    keywords_filter_raw = open(f"filters/{keywords}", "r").readlines()
    keywords_filter_nospace = [keyword.replace(" ", "|") for keyword in keywords_filter_raw]
    keywords_filter = [word.strip() for word in keywords_filter_nospace]
    # Create a single string from the list
    single_string = " OR ".join(keywords_filter)
    # Split the single string into multiple strings based on the maximum length
    split_strings = []
    start = 0
    while start < len(single_string):
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
        split_strings.append(single_string[start:end])
        start = end + 1
    split_strings_final = [keyword.replace("|", " ") for keyword in split_strings]
    return split_strings_final
