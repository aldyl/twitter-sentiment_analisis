#!/bin/python3

from tweets.tweets_snscrape import SnscrapeTwiteer
from tweets.tweets_handler import Tweets

sn = SnscrapeTwiteer()
tweet_handler = Tweets()

tweets = sn.get_by_query("mexico cubaimport asyncio",
                         2, since='2023-01-01', until='2023-03-29')

tweet_handler.tweet_to_json(tweets, 'util/file.json')

print(tweet_handler.get_most_used_words(tweets, 10 ))


