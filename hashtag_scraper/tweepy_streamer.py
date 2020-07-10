from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

from hashtag_scraper import twitter_credentials

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend_list)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(home_timeline_tweets)
        return home_timeline_tweets

    def get_hashtag_tweets(self, num_tweets):
        hashtag_tweets = []
        for tweet in Cursor(self.twitter_client.hashtag_tweets, id=self.twitter_user).items(num_tweets):
            hashtag_tweets.append(hashtag_tweets)
        return hashtag_tweets

    def get_trending_topic(self, num_trending):
        trending_topics = []
        for topic in Cursor(self.twitter_client.trending_topic, id=self.twitter_user).items(num_trending):
            trending_topics.append(trending_topics)
        return trending_topics


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


class TweetAnalyzer():

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        # df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['favorites'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        # df['source'] = np.array([tweet.source for tweet in tweets])
        # df['author'] = np.array([tweet.author for tweet in tweets])

        return df

    def clean_tweet(self, tweet):
        # Removing the special characters and hyperlinks from the tweet text
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment_cat(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def analyze_sentiment(self, tweet):
        analysis_pure = TextBlob(self.clean_tweet(tweet))
        return analysis_pure.sentiment.polarity

    def analyze_subjectivity(self, tweet):
        analysis_pure = TextBlob(self.clean_tweet(tweet))
        return analysis_pure.sentiment.subjectivity


if __name__ == "__main__":
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    # Get trending topics
    trends1 = api.trends_place(id=2388929)
    data = trends1[0]
    # grab the trends
    trends = data['trends']
    # grab the name from each trend
    names = [trend['name'] for trend in trends[:2]]
    print(names)
    trending = {}
    num_tweets = 3
    temp = []
    tweets = []
    for i in names:
        temp = api.search(q=i, count=num_tweets)
        for j in range(0, num_tweets):
            tweets.append(temp[j].text)

        trending[i] = tweets



    print(trending)
