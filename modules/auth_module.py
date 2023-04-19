import tweepy
import configparser

# read config.ini file
def get_auth(config_file, auth_method='OAuth2'):

    """
    Handles the Twitter API authentication process.

    Args:
        config_file (str): Path of the config file containing personal API details.
        auth_method (str): authentication method, either OAuth1 or OAuth2. Defaults to 'OAuth2'.

    Returns:
        dict: Dictionary with API keys and methods.
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    API_KEY = config['twitter API']['API_KEY']
    API_KEY_SECRET = config['twitter API']['API_KEY_SECRET']
    BEARER_TOKEN = config['twitter API']['BEARER_TOKEN']
    ACCESS_TOKEN = config['twitter API']['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = config['twitter API']['ACCESS_TOKEN_SECRET']

    # authentication
    client = tweepy.Client(bearer_token=BEARER_TOKEN, 
                           consumer_key=API_KEY, 
                           consumer_secret=API_KEY_SECRET, 
                           access_token=ACCESS_TOKEN, 
                           access_token_secret=ACCESS_TOKEN_SECRET)

    if auth_method == "OAuth2":
        auth = tweepy.OAuth2BearerHandler(bearer_token=BEARER_TOKEN)
    elif auth_method == "OAuth1":
        auth = tweepy.OAuth1UserHandler(consumer_key=API_KEY, 
                                        consumer_secret=API_KEY_SECRET, 
                                        access_token=ACCESS_TOKEN, 
                                        access_token_secret=ACCESS_TOKEN_SECRET)
    else:
        print("""error in the specification of the authentication method. \n
                 use 'OAuth2' for OAuth 2.0 Bearer Token (App only) and 'OAuth1' for 
                 OAuth 1.0a (User Context).""")

    api = tweepy.API(auth)

    auth_final = {"API": api,
                  "API_KEY": API_KEY,
                  "API_KEY_SECRET": API_KEY_SECRET,
                  "BEARER_TOKEN": BEARER_TOKEN,
                  "ACCESS_TOKEN": ACCESS_TOKEN,
                  "ACCESS_TOKEN_SECRET": ACCESS_TOKEN_SECRET}

    return(api, auth_final)


def load_config_multi(config_file):
    """
    Loads authentication credentials from a config file

    Args:
        config_file (str): Path of the config file containing personal API details.

    Returns:
        list of dict: Each dictionary represents the authentication credentials for a single set of API keys.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    auth_list = []
    for section in config.sections():
        auth_dict = {}
        for key, value in config.items(section):
            auth_dict[key] = value
        auth_list.append(auth_dict)
    
    return auth_list