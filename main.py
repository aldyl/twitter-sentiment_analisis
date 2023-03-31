#!/bin/python3

from model.mysql_connector import MysqlConnector
from tweets.tweets_snscrape import SnscrapeTwiteer
from tweets.tweets_handler import Tweets

sn = SnscrapeTwiteer()
tweet_handler = Tweets()

tweets = sn.get_by_query("dias canel",
                       10, since='2023-01-01', until='2023-03-29')

tweet_handler.tweet_to_json(tweets, 'util/file.json')

#print(tweet_handler.get_most_used_words(tweets, 10 ))

msql = MysqlConnector()
msql.connect()
msql.create_tweet_table()
msql.insert_tweet_on_table(tweets)
msql.close()