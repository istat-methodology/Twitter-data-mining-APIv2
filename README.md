# Twitter data mining (API v2)
A collection of Python scripts built around the [Tweepy](https://github.com/tweepy/tweepy) module to extract data from Twitter (API v2).

## Authentication
In order to get the authorization to stream Tweets we need to authenticate. Authentication is achieved through the personal API keys of the Twitter Developer account. There are different ways to authenticate through tweepy: in particular, tweepy's interface for Twitter API v2, `tweepy.Client`, automatically handles both OAuth 2.0 Bearer Token (application only) and OAuth 1.0a User Context authentication:
- **OAuth 2.0 Bearer Token (App only)** - with this authentication method you can make API requests on behalf of your Twitter Developer App using only the Bearer Token, with no connection to your user profile. This authentication method is suited for read-only access to public information, sucha as public Tweets. This authentication method is not suited to retrieve data that is not publicly available.
- **OAuth 1.0a (User Context)** - with this authentication method you can to make API requests on behalf of a Twitter user (yourself if the keys are obtained within your developer profile). This method requires you to use both the API Key and API Key Secret as well as the Access Token and the Access Token Secret as part of the authorization header in the API request.

In order to choose your preferred authentication method you should include it in your configuration file (config.ini) in the following way:
```
[twitter]

authentication_method = OAuth2
```
if you want to use the OAuth 2.0 Bearer Token (App only) authentication method, or:
```
[twitter]

authentication_method = OAuth1
```
if you wish to authenticate through the OAuth 1.0a (User Context) method.


More detailed information on the Twitter API v2 authentication methods can be found [here](https://developer.twitter.com/en/docs/authentication/overview).

#### How to authenticate
In order to authenticate with your credentials, store your keys into a config.ini file and move it into the `./auth` folder. The python script will authomatically read the config file and use the provided keys to proceed with the authorization. The config.ini file should have the following structure:
```
[twitter]

API_KEY = your api key
API_KEY_SECRET = your api key secret
BEARER_TOKEN = your bearer token
ACCESS_TOKEN = your access token
ACCESS_TOKEN_SECRET = your access token secret
```
Once the config file is set up, complete the authentication process calling the `get_auth` function from the `authentication` module:

```python
import authentication

auth = authentication.get_auth(config_file_path)
```
This function will automatically handle the authentication process based on the information provided in the config file.

## Rules
The rule handling module `rule_handler.py` automatically handles query and rule building based on a list of keywords and other parameters. 

## Tweet listener | _Filtered stream_
Access a real-time stream of tweets filtered by specific criteria. This powerful feature provides a way to monitor and analyze Twitter conversations in real-time, enabling developers to gain insights into trending topics, sentiment analysis, and other important metrics.

With Twitter API v2, developers can create filtered streams based on specific keywords, hashtags, geographic locations, languages, and more. The API delivers a continuous stream of tweets that match the specified criteria, making it an ideal solution for monitoring live events or analyzing social media sentiment.

### Set up a filtered stream

We need to define a custom `MyStreamListener` class that inherits from `tweepy.StreamListener`. For example:

```python
class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api):
        super().__init__(api=api)
        self.tweet_count = 0
    
    def on_status(self, status):
        self.tweet_count += 1
        remaining_tweets = api.rate_limit_status()['resources']['/statuses/filter']['remaining']
        print(f"{tweet_count} tweets downloaded during the current stream. {remaining_tweets} tweets left.")
    
    def on_error(self, status_code):
        if status_code == 420;
            print("Rate limited. Disconnecting...")
            return False
```

- The `on_status` method is called whenever a new tweet is received by the stream. In this method, we increment the `tweet_count` variable, and then update `remaining_tweets` by calling `rate_limit_status()` on the API object.
- The `on_error` method is called whenever an error occurs with the stream. If the error code is 420 (rate limited), we print a message and return `False` to disconnect the stream.

As the stream runs, the `on_status` method is called for each incoming tweet, and `remaining_tweets` is updated in real-time.
