# Twitter-Public-Analysis

Hey! We're working on making a twitter analysis tool that can analyze tweets in real time and give us valuable insights

Interested in working with us? Join our discord [here](https://discord.com/channels/729368876965429310/729368876965429313)!

## Getting Started

Getting started shouldn't be too hard. Here are the steps:

1. Clone the repository

`git clone https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis.git`

2. Install the requirements

`pip install -r requirements.txt`

3. Configure the twitter settings

Follow the steps [here](https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/blob/master/config/README.md) to add your twitter credentials. Don't worry, we're working on removing this step

4. We need to actually getting it running

`python sentiment_analysis_app.py --topic-counts 3 --tweets-count 100 --clean-tweets True`

4.5 Here's the `help` from the sentiment analysis app:
```
usage: sentiment_analysis_app.py [-h] [--topic-counts TOPICS_COUNT]
                                 [--tweets-count TWEETS_COUNT]
                                 [--clean-tweets CLEAN_TWEETS]

optional arguments:
  -h, --help            show this help message and exit
  --topic-counts TOPICS_COUNT
                        number of topics to download for
  --tweets-count TWEETS_COUNT
                        number of tweets to grab per topic
  --clean-tweets CLEAN_TWEETS
                        clean the tweets before analyzing them
```
