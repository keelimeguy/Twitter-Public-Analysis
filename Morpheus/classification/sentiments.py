from typing import Dict

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import flair

nltk.download('vader_lexicon', quiet=True)
NLTK_SENTIMENT_INTENSITY_ANALYZER = SentimentIntensityAnalyzer()
flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

"""
Author: v2thegreat

Tutorial Followed: https://medium.com/@b.terryjack/nlp-pre-trained-sentiment-analysis-1eb52a9d742c

Libraries Used:
 - NLTK
 - TextBlob
 - Flair
"""


class Sentiments:
    @classmethod
    def sentiment_analysis_nltk(cls, text: str) -> float:
        """
        Run sentiment analysis using the library NLTK. Runs default sentiment on vader lexicon

        Works based on bag of words and positive and negative word lookups
        :param text: text to be analysed
        :return: sentiment compound for given text
        """
        return NLTK_SENTIMENT_INTENSITY_ANALYZER.polarity_scores(text=text)['compound']

    @classmethod
    def sentiment_analysis_textblob(cls, text: str) -> float:
        """
        Run sentiment analysis using the library textblob. Returns default sentiment

        Works similar to NLTK's sentiment analysis, but includes subjectivity analysis
        :param text: text to be analysed
        :return: sentiment for given text
        """
        return TextBlob(text=text).sentiment.polarity

    @classmethod
    def sentiment_analysis_flair(cls, text: str) -> float:
        """
        Run sentiment analysis using the library flair. Returns default sentiment

        Works based on a character-level LSTM neural network
        :param text: text to be analysed
        :return: sentiment for given text
        """
        if not text:
            return 0

        s = flair.data.Sentence(text)
        flair_sentiment.predict(s)
        total_sentiment = s.labels
        if total_sentiment[0].value == 'NEGATIVE':
            return total_sentiment[0].score * -1
        else:
            return total_sentiment[0].score

    @staticmethod
    def multiple_sentiment_analysis(text: str) -> Dict[str, float]:
        return {sentiment: _sentiment_functions[sentiment](text) for sentiment in
                _sentiment_functions.keys()}


_sentiment_functions = {
    'nltk': Sentiments.sentiment_analysis_nltk,
    'textblob': Sentiments.sentiment_analysis_textblob,
    'flair': Sentiments.sentiment_analysis_flair
}

if __name__ == "__main__":
    sentence = 'The world is not a good place'
    print(Sentiments.sentiment_analysis_nltk(sentence))
    print(Sentiments.sentiment_analysis_textblob(sentence))
    print(Sentiments.sentiment_analysis_flair(sentence))
