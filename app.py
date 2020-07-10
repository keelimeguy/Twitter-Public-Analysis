import pandas as pd
from tqdm import tqdm

from sentiment_analysis_tools import Sentiments

tweets_dict = {}

dataframe = pd.Dataframe(columns=['topic_name', 'tweets'])

for topic in tqdm(tweets_dict.keys()):
    tweets = pd.Series(tweets_dict[topic])
    topics = pd.Series([topic] * tweets.size)
    dataframe.append((topics, tweets))

sentiments = [ Sentiments.multiple_sentiment_analysis(tweet) for tweet in dataframe.tweets.iterrows()]

dataframe = dataframe.concat(sentiments)

if __name__ == "__main__":
    print(dataframe)
