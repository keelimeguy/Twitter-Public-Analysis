import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

NLTK_SENTIMENT_INTENSITY_ANALYZER = SentimentIntensityAnalyzer()

from textblob import TextBlob

import flair

flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

"""
Author: v2thegreat

Source: https://medium.com/@b.terryjack/nlp-pre-trained-sentiment-analysis-1eb52a9d742c

Libraries Used:
 - NLTK
 - TextBlob
 - Flair
"""


def sentiment_analysis_nltk(text: str) -> float:
    """
    Run sentiment analysis using the library NLTK. Runs default sentiment on vader lexicon

    Works based on bag of words and positive and negative word lookups
    :param text: text to be analysed
    :return: sentiment compound for given text
    """
    return NLTK_SENTIMENT_INTENSITY_ANALYZER.polarity_scores(text=text)['compound']


def sentiment_analysis_textblob(text: str) -> float:
    """
    Run sentiment analysis using the library textblob. Returns default sentiment

    Works similar to NLTK's sentiment analysis, but includes subjectivity analysis
    :param text: text to be analysed
    :return: sentiment for given text
    """
    return TextBlob(text=text).sentiment.polarity


def sentiment_analysis_flair(text: str) -> float:
    """
    Run sentiment analysis using the library flair. Returns default sentiment

    Works based on a character-level LSTM neural network
    :param text: text to be analysed
    :return: sentiment for given text
    """
    s = flair.data.Sentence(text)
    flair_sentiment.predict(s)
    total_sentiment = s.labels
    if total_sentiment[0].value == 'NEGATIVE':
        return total_sentiment[0].score * -1
    else:
        return total_sentiment[0].score


if __name__ == "__main__":
    sentence = 'The world is not a good place'
    print(sentiment_analysis_nltk(sentence))
    print(sentiment_analysis_textblob(sentence))
    print(sentiment_analysis_flair(sentence))
