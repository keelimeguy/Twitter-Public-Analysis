from typing import Dict

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import flair
from pprint import pprint

"""
Author: v2thegreat

Source: https://medium.com/@b.terryjack/nlp-pre-trained-sentiment-analysis-1eb52a9d742c

Libraries Used:
 - NLTK
 - TextBlob
 - Flair
"""


class Sentiments:

    __instance__ = None

    def __init__(self):
        if Sentiments.__instance__ is None:
            Sentiments.__instance__ = self

            nltk.download('vader_lexicon', quiet=True)
            self.NLTK_SENTIMENT_INTENSITY_ANALYZER = SentimentIntensityAnalyzer()
            self.flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

        else:
            raise RuntimeError("singleton Sentiments class is created more than once!")

    @staticmethod
    def get_instance():
        """Returns a singleton instance of this Sentiments class
        """
        if not Sentiments.__instance__:
            Sentiments()
        return Sentiments.__instance__

    @staticmethod
    def sentiment_analysis_nltk(text: str) -> float:
        """
        Run sentiment analysis using the library NLTK. Runs default sentiment on vader lexicon

        Works based on bag of words and positive and negative word lookups
        :param text: text to be analyzed
        :return: sentiment compound for given text
        """
        if not text:
            return 0

        return Sentiments.get_instance().NLTK_SENTIMENT_INTENSITY_ANALYZER.polarity_scores(text=text)['compound']

    @staticmethod
    def sentiment_analysis_textblob(text: str) -> float:
        """
        Run sentiment analysis using the library textblob. Returns default sentiment

        Works similar to NLTK's sentiment analysis, but includes subjectivity analysis
        :param text: text to be analyzed
        :return: sentiment for given text
        """
        if not text:
            return 0

        return TextBlob(text=text).sentiment.polarity

    @staticmethod
    def sentiment_analysis_flair(text: str) -> float:
        """
        Run sentiment analysis using the library flair. Returns default sentiment

        Works based on a character-level LSTM neural network
        :param text: text to be analyzed
        :return: sentiment for given text
        """
        if not text:
            return 0

        s = flair.data.Sentence(text)
        Sentiments.get_instance().flair_sentiment.predict(s)
        total_sentiment = s.labels
        if total_sentiment[0].value == 'NEGATIVE':
            return total_sentiment[0].score * -1
        else:
            return total_sentiment[0].score

    _sentiment_function_mapping = {
        'nltk': sentiment_analysis_nltk.__func__,
        'textblob': sentiment_analysis_textblob.__func__,
        'flair': sentiment_analysis_flair.__func__
    }

    @classmethod
    def multiple_sentiment_analysis(cls, text: str) -> Dict[str, float]:
        return {sentiment: sentiment_function(text) for sentiment, sentiment_function in
                cls._sentiment_function_mapping.items()}


if __name__ == "__main__":
    _sentence = 'The world is not a good place'
    pprint(Sentiments.multiple_sentiment_analysis(_sentence))
