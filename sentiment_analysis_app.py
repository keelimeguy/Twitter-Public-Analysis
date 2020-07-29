import pandas as pd
from tqdm import tqdm
from sentiment_analysis_tools import Sentiments
from hashtag_scraper import tweepy_streamer

print('\nFetching tweets, this might take a moment')

TOPICS_COUNT = 5
NUMBER_OF_TWEETS_PER_TOPIC = 100
tweets_dict = tweepy_streamer.fetch_tweets(TOPICS_COUNT, NUMBER_OF_TWEETS_PER_TOPIC)

tweets_count = sum([len(tweets_dict[list(tweets_dict.keys())[x]]) for x in range(TOPICS_COUNT)])
tweets_count = tweets_count / TOPICS_COUNT
print(f"\nGot {tweets_count} tweets for each topic. Originally tried to get {NUMBER_OF_TWEETS_PER_TOPIC} per topic")

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

if __name__ == "__main__":
    print(sentiments.groupby('topic_name').agg(['mean', 'min', 'max']).to_string())
