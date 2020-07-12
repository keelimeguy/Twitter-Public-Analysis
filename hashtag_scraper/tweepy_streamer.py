from tweepy import API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import time


from hashtag_scraper import twitter_credentials

# Function to clean a tweet of special characters and hyperlinks
def clean_tweet(tweet):
    # Removing the special characters and hyperlinks from the tweet text
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet).split())

def fetch_tweets():
    #
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()

    # Get trending topics per Geo location ID
    trends1 = api.trends_place(id=2388929)
    data = trends1[0]

    # grab the trends
    trends = data['trends']

    # grab the name from each trend
    names = [trend['name'] for trend in trends[:10]]

    # Debug => prints trending list
    # print(names)

    # number of tweets to be gathered per trending topic
    num_tweets = 25

    # Initialize dict for trending topic and respective tweets
    trending = {}
    temp = []
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



class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client



class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


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


class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False

        print(status)

