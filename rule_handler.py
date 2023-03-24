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

def add_rules(keywords, api):
    keyword_filter_raw = open(f"filters/{keywords}", "r").readlines()
    keyword_filter = [word.strip() for word in keyword_filter_raw]
    keyword_filter_string = ' OR '.join(keyword_filter)

    if api == 'elevated':
        truncated_filter = ""
        index = 0
        if len(keyword_filter_string) > 512: # forse conviene mettere 512+4? (per l'ultimo ' OR ')
            while len(truncated_filter) <= 512: # forse conviene mettere 512+4? (per l'ultimo ' OR ')
                    if index <= len(keyword_filter):
                        truncated_filter += f"{str(keyword_filter[index])} OR "
                    else:
                         print("ERROR: index exceeds filter")
                    index = index + 1 
    print(truncated_filter[:len(truncated_filter) -4])  # removes the last ' OR '