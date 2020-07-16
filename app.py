import pandas as pd
from tqdm import tqdm

from sentiment_analysis_tools import Sentiments

tweets_dict = {'abcd': ['The world is not a good place', 'I hate you!']}

all_topics = []
all_tweets = []

for topic in tweets_dict.keys():
    all_topics.extend([topic] * len(tweets_dict[topic]))
    all_tweets.extend(tweets_dict[topic])

dataframe = {'topic_name': all_topics, 'tweets': all_tweets}

sentiments = pd.DataFrame([Sentiments.multiple_sentiment_analysis(tweet) for tweet in tqdm(dataframe['tweets'])])

sentiments['tweets'] = dataframe['tweets']
sentiments['topic_name'] = dataframe['topic_name']

if __name__ == "__main__":
    print(sentiments.groupby('topic_name').agg('mean'))
