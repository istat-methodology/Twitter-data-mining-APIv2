# Filtered Stream template - Work in progress

import modules.auth_module as auth_module
import modules.rule_handler as rule_handler
import modules.stream_builder as stream_builder

api_tier = 'elevated'
data_detail = 'text'
launch_stream = False

# Enter your API keys and access tokens
auth = auth_module.get_auth(config_file="config/config.ini", 
                               auth_method="OAuth2")
api = auth[0]
auth_keys = auth[1]

# Set up the filtered stream
listener = stream_builder.stream_builder(bearer_token=auth_keys['BEARER_TOKEN'],
                                         display_text=True,
                                         store_data=False,
                                         wait_on_rate_limit=True)

# Define the filter rules
keyword_list_1 = ['put', 'your keywords', 'here']
keyword_list_2 = ['put', 'other keywords', 'here']
rules = [keyword_list_1, keyword_list_2]

listener = rule_handler.rule_handler(tweet_listener=listener, 
                                     keywords=rules, 
                                     api_tier=api_tier, 
                                     language='it', 
                                     query='')

# launch the listener and choose what to store
if launch_stream == True:
    stream_builder.stream_launcher(tweet_listener=listener,
                                   detail=data_detail)