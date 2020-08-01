import re


class TweetFormatting:
    REMOVE_SYMBOLS_RE = "RT (@[A-Za-z0-9]+)"

    @classmethod
    def _remove_symbols(cls, tweet):
        """
        Cleans the tweet using regular expression for special characters or hyperlinks.

        :param tweet: text to be processed
        :return: text without special characters or hyperlinks
        """

        return ' '.join(re.sub(cls.REMOVE_SYMBOLS_RE, " ", tweet).split())

    @classmethod
    def clean_tweet(cls, tweet):
        return cls._remove_symbols(tweet)
