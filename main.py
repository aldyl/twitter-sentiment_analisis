#!/bin/python3

from tweets.tweets_snscrape import SnscrapeTwiteer

sn = SnscrapeTwiteer()

tweets = sn.get_by_query("trending topic mexico",
                         100, since='2023-01-01', until='2023-03-29')
sn.tweet_to_json(tweets, 'util/file.json')
print(sn.get_most_used_words(tweets, 3 ))



