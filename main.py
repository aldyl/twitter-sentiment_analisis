#!/bin/python3

import datetime
from tweets.tweets_handler import Tweets


tweet_handler = Tweets()

#Id, Date, Content, Impact, Polarity, Objective
query = "CocaCola"
table = query.replace(" ","_")
max_retrieve_tweets = 10

startDate = datetime.datetime(2023, 1, 1)
stopDate = datetime.datetime(2023, 3, 31)


tweet_handler.get_by_query(query=query, cant=max_retrieve_tweets, since=startDate.isoformat(), until=stopDate.isoformat())





data = 'Content'
tweets = msql.get_tweet_timelapse_bd(table=table, columns=data, since=startDate, until=stopDate)
tweet_handler.get_most_used_words(tweets, 20, "util/common_words.png")


data = 'Polarity'
tweets = msql.get_tweet_timelapse_bd(table=table, columns=data, since=startDate, until=stopDate)

tweet_df = tweet_handler.tweet_to_json(tweets, "util/data.json", columns=[data])

tweet_handler.get_tweet_data_frecuency(tweet_df, data, query, "bar", "util/chart_data.png")

msql.close()