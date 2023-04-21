# Twitter Data Mining (API v2)
A collection of Python scripts built around the [Tweepy](https://github.com/tweepy/tweepy) module to extract data from Twitter (API v2).

## Tweet Listener with Keyword Filtering (Filtered Stream endpoint)

This Python code sets up a Twitter API listener using the Tweepy library to collect and filter tweets containing specific keywords. The listener connects to the Twitter API using a bearer token and filters tweets based on lists of keywords stored in text files.

### Prerequisites

Before running this code, you need to have a Twitter Developer account and create an app to generate a bearer token. You also need to install the following Python packages:

    tweepy
    json
    os
    typing
    datetime

### Usage

To use this code, first fill in your Twitter API bearer token in the `bearer_token` variable. This token is necessary for authentication and authorization to use the Twitter API.

Next, specify the path to the directory containing the filter files in `wordlist_path`. The keyword lists for filtering are stored text files. These files contain one keyword per line. You can modify these files to include or exclude specific keywords based on your filtering needs. The script is set up to filter on two different sets of keywords and assign different rule tags.

By default, `launch_stream` is set to `False`, meaning that the listener will not be launched when you run the script. If you want to activate the listener and start collecting data, set this value to `True`.

The `store_data` variable determines whether or not the filtered tweets will be stored as JSON files in the `data` directory. If this value is `True`, the code will check if the `data` directory exists and create it if necessary. If it already exists, it will use it to store the data.

When the listener is running, it will print a message to the console to confirm that it has connected successfully. It will also create a new JSON file for each hour of data received, with a filename based on the current date and time. Each JSON file contains a list of tweets that passed through the filtering rules.

### Listener Options

The listener uses the `TweetListener` class, which extends Tweepy's `StreamingClient` class. The `TweetListener` class has three methods that can be overridden:

- `on_connect`: This method is called when the listener successfully connects to the Twitter API. It prints a message to the console and creates a new directory to store the data if `store_data` is True.

- `on_data`: This method is called when the listener receives a new tweet that passes through the filtering rules. If `store_data` is `True`, it stores the tweet in a JSON file in the `data` directory. The JSON file is named based on the current date and time.

- `on_errors`: This method is called when the listener encounters an error. If the error code is 400 (Usage cap exceeded), the method returns False to stop the listener.

## Query Handler Module

The `QueryHandler` class is used to set up the filter rules based on the keyword lists. The class has the following methods:

- `query_builder`: This method takes a list of keywords and builds a query for filtering tweets that contain any of the keywords. The method returns a dictionary containing the filter rules.

- `clean_rules`: This method removes any existing filter rules associated with the listener.

- `push_rules`: This method adds new filter rules to the listener. It takes a list of rules and a tag for the rules as arguments. The method returns the updated listener.
