# Twitter data mining (API v2)
A collection of Python scripts built around the [Tweepy](https://github.com/tweepy/tweepy) module to extract data from Twitter (API v2).

## Tweet listener
The tweet listener is used to stream tweets in real-time filtering them based on a set of rules. Rules include keywords, language, geolocalization and more. Tweets are stored in json files, where a new json file is created for the specified time interval and updated in real-time.

## Authentication
In order to get the authorization to stream Tweets we need to authenticate. Authentication is achieved through the personal API keys of the Twitter Developer account. There are different ways to authenticate through tweepy: in particular, tweepy's interface for Twitter API v2, `Client`, automatically handles both OAuth 2.0 Bearer Token (application only) and OAuth 1.0a User Context authentication.
