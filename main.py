#!/bin/python3

import datetime

from model.mysql_connector import MysqlConnector
from tweets.tweets_snscrape import SnscrapeTwiteer
from tweets.tweets_handler import Tweets

sn = SnscrapeTwiteer()
tweet_handler = Tweets()

#Id, Date, Content, Impact, Polarity, Objective
query = "CocaCola"
data = 'Polarity'
max_retrieve_tweets = 100
startDate = datetime.datetime(2023, 1, 1)
stopDate = datetime.datetime(2023, 3, 31)

tweets = sn.get_by_query( query, max_retrieve_tweets, since=startDate, until=stopDate)

#tweet_handler.tweet_to_json(tweets, 'util/file.json')

print(tweet_handler.get_most_used_words(tweets, 10 ))

msql = MysqlConnector()
msql.connect()
#msql.create_tweet_table()
#msql.insert_tweet_on_table(tweets)



tweets = msql.get_tweet_timelapse_bd(columns=data, since=startDate, until=stopDate)

tweet_df = tweet_handler.tweet_to_json(tweets, "con.json", columns=[data])

IQR = tweet_handler.get_tweet_data_frecuency(tweet_df, data, query, "bar", "util/chart_data.png")
print(IQR)

msql.close()