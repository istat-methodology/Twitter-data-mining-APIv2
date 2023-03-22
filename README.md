# Twitter data mining (API v2)
A collection of Python scripts built around the [Tweepy](https://github.com/tweepy/tweepy) module to extract data from Twitter (API v2).

## Authentication
In order to get the authorization to stream Tweets we need to authenticate. Authentication is achieved through the personal API keys of the Twitter Developer account. There are different ways to authenticate through tweepy: in particular, tweepy's interface for Twitter API v2, `tweepy.Client`, automatically handles both OAuth 2.0 Bearer Token (application only) and OAuth 1.0a User Context authentication:
- **OAuth 2.0 Bearer Token (App only)** - with this authentication method you can make API requests on behalf of your Twitter Developer App using only the Bearer Token, with no connection to your user profile. This authentication method is suited for read-only access to public information, sucha as public Tweets. This authentication method is not suited to retrieve data that is not publicly available.
- **OAuth 1.0a (User Context)** - with this authentication method you can to make API requests on behalf of a Twitter user (yourself if the keys are obtained within your developer profile). This method requires you to use both the API Key and API Key Secret as well as the Access Token and the Access Token Secret as part of the authorization header in the API request.

In order to choose your preferred authentication method you should include it in your configuration file (config.ini) in the following way:
```
[twitter]

authentication_method = "OAuth2"
```
if you want to use the OAuth 2.0 Bearer Token (App only) authentication method, or:
```
[twitter]

authentication_method = "OAuth1"
```
if you wish to authenticate through the OAuth 1.0a (User Context) method.


More detailed information on the Twitter API v2 authentication methods can be found [here](https://developer.twitter.com/en/docs/authentication/overview).

### How to authenticate
In order to authenticate with your credentials, store your keys into a config.ini file and move it into the `./auth` folder. The python script will authomatically read the config file and use the provided keys to proceed with the authorization. The config.ini file should have the following structure:
```
[twitter]

API_KEY = "your api key"
API_KEY_SECRET = "your api key secret"
BEARER_TOKEN = "your bearer token"
ACCESS_TOKEN = "your access token"
ACCESS_TOKEN_SECRET = "your access token secret"
```

## Tweet listener | _Filtered stream_
The tweet listener is used to stream tweets in real-time filtering them based on a set of rules. Rules include keywords, language, geolocalization and more. Tweets are stored in json files, where a new json file is created for the specified time interval and updated in real-time.
