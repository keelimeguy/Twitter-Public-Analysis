import unittest

from sentiment_analysis_tools import Sentiments
import math


class SentimentsTestCase(unittest.TestCase):
    def test_multiple_sentiment_analysis_empty(self):
        expected_output = {
            'nltk': math.nan,
            'textblob': math.nan,
            'flair': math.nan
        }

        self.assertEqual(expected_output, Sentiments.multiple_sentiment_analysis(''))


if __name__ == "__main__":
    unittest.main()
