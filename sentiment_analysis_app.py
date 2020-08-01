import argparse
import pandas as pd
from tqdm import tqdm
from sentiment_analysis_tools import Sentiments
from hashtag_scraper import tweepy_streamer

TOPICS_COUNT = 5
TWEETS_COUNT = 20


def run_sentiment_analysis(topics_count: int = TOPICS_COUNT,
                           number_of_tweets_per_topic: int = TWEETS_COUNT):
    print('\nFetching tweets, this might take a moment')
    tweets_dict = tweepy_streamer.fetch_tweets(topics_count, number_of_tweets_per_topic)

    tweets_count = sum([len(tweets_dict[list(tweets_dict.keys())[x]]) for x in range(topics_count)])
    tweets_count = tweets_count / topics_count
    print(
        f"\nGot {tweets_count} tweets for each topic. Originally tried to get {number_of_tweets_per_topic} per topic")

    all_topics = []
    all_tweets = []

    for topic in tweets_dict.keys():
        all_topics.extend([topic] * len(tweets_dict[topic]))
        all_tweets.extend(tweets_dict[topic])

    topics_tweets_dataframe = {'topic_name': all_topics, 'tweets': all_tweets}

    sentiments = pd.DataFrame([Sentiments.multiple_sentiment_analysis(tweet) for tweet in
                               tqdm(topics_tweets_dataframe['tweets'],
                                    desc='Running Sentiment Analysis')])

    sentiments['tweets'] = topics_tweets_dataframe['tweets']
    sentiments['topic_name'] = topics_tweets_dataframe['topic_name']

    return sentiments.groupby('topic_name').agg(['mean', 'min', 'max']).to_string()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic-counts', default=TOPICS_COUNT, dest='topics_count', type=int,
                        help='number of topics to download for')
    parser.add_argument('--tweets-count', default=TWEETS_COUNT, dest='tweets_count', type=int,
                        help='number of tweets to grab per topic')
    args = parser.parse_args()
    print(run_sentiment_analysis(args.topics_count, args.tweets_count))
