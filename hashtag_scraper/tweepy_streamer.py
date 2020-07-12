from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re

from hashtag_scraper import twitter_credentials


def clean_tweet(tweet):
    """
    Cleans the tweet using regular expression for special characters or hyperlinks.

    :param tweet: text to be processed
    :return: text without special characters or hyperlinks
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet).split())


def fetch_tweets(num_topics, num_tweets, geo_code=2388929):
    """
    Fetches a number of tweets on a specified number of trending topics using a particular geo code.

    :param num_topics: Number of treading topics to be collected.
    :param num_tweets: Number of tweets per topic to be collected.
    :param geo_code: Geo code to get trending topics for that area.
    :return: Fetches a number of tweets on a specified number of tweets per a specified number of topics from a list of trending topics at a location.
    """
    # Creating an instance of
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()

    # Get trending topics per Geo location ID
    trends1 = api.trends_place(id=geo_code)
    data = trends1[0]

    # grab the trends
    trends = data['trends']

    # grab the name from each trend
    names = [trend['name'] for trend in trends[:num_topics]]

    # Debug => prints trending list
    # print(names)

    # number of tweets to be gathered per trending topic

    # Initialize dict for trending topic and respective tweets
    trending = {}
    tweets = []

    # Nest loop for searching each trending topic and then inserting those tweets into 'trending' dict
    for i in names:
        temp = api.search(q=i, count=num_tweets+1)

        # Debug => prints text content of tweet of specified index
        # print(temp[0].text)

        for j in range(0, num_tweets):
            tweets.append(clean_tweet(temp[j].text))
        trending[i] = tweets

    print(trending)


"""
This class contains basic functions to authenticate using the TwitterAuthenticator class. 
"""


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        """
        Modular function to return authentication keys to API function in the tweepy library.

        :return: starts the authentication process by calling TwitterAuthenticator class
        """
        return self.twitter_client


"""
This class contains a function to fetch authentication keys from 'twitter_credentials.py' and serve along side the TwitterClient class.
"""


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        """
        A modular function that gets called on to authenticate to Twitter API

        :return: Fetches Twitter API keys from twitter_credentials and uses OAuthHandler from tweepy library to authenticate Twitter API.
        """
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


"""
This class automatically passes the TwitterAuthenticator and TwitterListener to connect to the Twitter API.
"""


class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator

    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API.
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twiiter_app()
        stream = Stream(auth, listener)

        # this filters tweets, inside track can be a list of stuff to include inside the listener
        stream.filter(track=hash_tag_list)


"""
This class listens to the response from the Twitter API for any important codes or exceptions that are raised. 
"""


class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        """
        Listens to the Twitter API response to output

        :param data: Response from Twitter API
        :return: prints response from Twitter API
        """
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        """
        Monitors the Twitter API for any error codes.
            - Breaks if code equals 420 (rate limit raised)

        :param status: Status codes from Twitter API
        :return: Status codes from Twitter API
        """
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False

        print(status)