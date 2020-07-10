import pandas as pd
from tqdm import tqdm

from sentiment_analysis_tools import Sentiments, _sentiment_functions

tweets_dict = {'abcd': ['I hate this website', 'I hate you!']}

all_topics = []
all_tweets = []

for topic in tqdm(tweets_dict.keys()):
    all_topics.extend(tweets_dict[topic])
    all_tweets.extend([topic] * len(tweets_dict[topic]))

dataframe = {'topic_name': all_topics, 'tweets': all_tweets}

sentiments = pd.DataFrame([Sentiments.multiple_sentiment_analysis(tweet) for tweet in dataframe['tweets']])

sentiments['tweets'] = dataframe['tweets']
sentiments['topic_name'] = dataframe['topic_name']

if __name__ == "__main__":
    print(sentiments)
