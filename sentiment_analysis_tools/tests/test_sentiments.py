import unittest

from sentiment_analysis_tools import Sentiments


class SentimentsTestCase(unittest.TestCase):
    def test_multiple_sentiment_analysis_empty(self):
        expected_output = {
            'nltk': 0,
            'textblob': 0,
            'flair': 0
        }

        self.assertEqual(expected_output, Sentiments.multiple_sentiment_analysis(''))


if __name__ == "__main__":
    unittest.main()
