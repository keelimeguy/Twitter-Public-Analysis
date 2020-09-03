import argparse
from typing import Dict
import pandas as pd
from tqdm import tqdm
from Morpheus.classification.sentiment_analysis import Sentiments

TOPICS_COUNT = 5
TWEETS_COUNT = 20


def _get_average_tweets_per_topic(tweets_dict: Dict, topics_count: int) -> float:
    tweets_count_per_topic = [len(tweets_dict[list(tweets_dict.keys())[x]]) for x in
                              range(topics_count)]
    total_tweets_count = sum(tweets_count_per_topic)
    return total_tweets_count / topics_count


def _format_tweets(tweets_dict):
    all_topics = []
    all_tweets = []

    for topic in tweets_dict.keys():
        all_topics.extend([topic] * len(tweets_dict[topic]))
        all_tweets.extend(tweets_dict[topic])

    topics_tweets_dict = {'topic_name': all_topics, 'tweets': all_tweets}
    return topics_tweets_dict


def _get_sentiments(topics_tweets_dict):
    sentiments_progress_bar = tqdm(topics_tweets_dict['tweets'], desc='Running Sentiment Analysis')
    sentiments = [Sentiments.multiple_sentiment_analysis(tweet) for tweet in sentiments_progress_bar]
    sentiments = pd.DataFrame(sentiments)

    sentiments['tweets'] = topics_tweets_dict['tweets']
    sentiments['topic_name'] = topics_tweets_dict['topic_name']

    return sentiments


def run_sentiment_analysis(topics_count: int = TOPICS_COUNT,
                           number_of_tweets_per_topic: int = TWEETS_COUNT,
                           clean_tweets=True) -> str:
    print('\nFetching tweets, this might take a moment')
    tweets_dict = tweepy_streamer.fetch_tweets(topics_count, number_of_tweets_per_topic, clean_tweets=clean_tweets)

    print(f"\nGot {_get_average_tweets_per_topic(tweets_dict, topics_count)} tweets for each topic."
          f" Originally tried to get {number_of_tweets_per_topic} per topic")

    topics_tweets_dict = _format_tweets(tweets_dict)

    sentiments = _get_sentiments(topics_tweets_dict)

    return sentiments.groupby('topic_name').agg(['mean', 'min', 'max']).to_string()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic-counts', default=TOPICS_COUNT, dest='topics_count', type=int,
                        help='number of topics to download for')
    parser.add_argument('--tweets-count', default=TWEETS_COUNT, dest='tweets_count', type=int,
                        help='number of tweets to grab per topic')
    parser.add_argument('--clean-tweets', default=TWEETS_COUNT, dest='clean_tweets', type=bool,
                        help='clean the tweets before analyzing them')
    args = parser.parse_args()
    print(run_sentiment_analysis(args.topics_count, args.tweets_count, args.clean_tweets))
