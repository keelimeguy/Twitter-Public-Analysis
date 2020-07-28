import re
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from config import config


class _TwitterClient:
    """
    This class contains basic functions to authenticate using the TwitterAuthenticator class.
    """

    def __init__(self, twitter_user=None):
        self.auth = _TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        """
        Modular function to return authentication keys to API function in the tweepy library.

        :return: starts the authentication process by calling TwitterAuthenticator class
        """
        return self.twitter_client


class _TwitterAuthenticator:
    """
    This class contains a function to fetch authentication keys from 'twitter_credentials.py' and serve along side the TwitterClient class.
    """

    @classmethod
    def authenticate_twitter_app(cls):
        """
        A modular function that gets called on to authenticate to Twitter API

        :return: Fetches Twitter API keys from twitter_credentials and uses OAuthHandler from tweepy library to authenticate Twitter API.
        """
        auth = OAuthHandler(config.API_KEY, config.API_SECRET_KEY)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        return auth


class _TwitterStreamer:
    """
    This class automatically passes the TwitterAuthenticator and TwitterListener to connect to the Twitter API.
    """

    def __init__(self):
        self.twitter_authenticator = _TwitterAuthenticator

    def stream_tweets(self, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API.
        listener = _TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # this filters tweets, inside track can be a list of stuff to include inside the listener
        stream.filter(track=hash_tag_list)


class _TwitterListener(StreamListener):
    """
    This class listens to the response from the Twitter API for any important codes or exceptions that are raised.
    """

    def __init__(self, fetched_tweets_filename):
        super().__init__()
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


def _clean_tweet(tweet):
    """
    Cleans the tweet using regular expression for special characters or hyperlinks.

    :param tweet: text to be processed
    :return: text without special characters or hyperlinks
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet).split())


def fetch_tweets(num_topics: int, num_tweets: int, geo_code: int = 2388929,
                 clean_tweets: bool = True):
    """
    Fetches a number of tweets on a specified number of trending topics using a particular geo code.

    :param num_topics: Number of treading topics to be collected.
    :param num_tweets: Number of tweets per topic to be collected.
    :param geo_code: Geo code to get trending topics for that area.
    :param clean_tweets: Should we automatically clean the tweet?
    :return: Fetches a number of tweets on a specified number of tweets per a specified number of topics from a list of trending topics at a location.
    """
    # Creating an instance of
    twitter_client = _TwitterClient()
    api = twitter_client.get_twitter_client_api()

    # Get trending topics per Geo location ID
    trends_place = api.trends_place(id=geo_code)
    data = trends_place[0]

    # grab the trends
    trends = data['trends']

    # grab the name from each trend
    names = [trend['name'] for trend in trends[:num_topics]]

    # Debug => prints trending list
    # print(names)

    # number of tweets to be gathered per trending topic

    # Initialize dict for trending topic and respective tweets
    trending = {}

    # Nest loop for searching each trending topic and then inserting those tweets into 'trending' dict
    for name in names:
        tweets = []
        temp = api.search(q=name, count=num_tweets + 1)
        # Debug => prints text content of tweet of specified index
        # print(temp[0].text)

        for j in range(num_tweets):
            if clean_tweets:
                tweets.append(_clean_tweet(temp[j].text))
            else:
                tweets.append(temp[j].text)

        trending[name] = tweets

    return trending


if __name__ == '__main__':
    pass
