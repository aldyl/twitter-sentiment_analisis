#!/bin/python3
import datetime
from tweets.tweets_handler import Tweets

table = "Coca"
query = "CocaCola"
max_retrieve_tweets = 50000
startDate = datetime.datetime(2023, 1, 1)
stopDate = datetime.datetime(2023, 3, 31)


tweet_handler = Tweets(table=table)

tweet_handler.load_internet_data(query=query,
                                 max_retrieve_tweets=max_retrieve_tweets,
                                 since=startDate, until=stopDate, max_descargas=10000)

print("¿Cuáles son las 10 palabras más empleadas?\n")
print(tweet_handler.get_most_used_words(
    since=startDate, until=stopDate, cant=50, img_src="result/common_words.png"))

print("¿Qué sentimiento es más intenso?")
print(tweet_handler.get_more_intense_sentiment(
    since=startDate, until=stopDate, img_src="result/more_intense_sentiment.png"))

print("¿Qué tan objetivos son los Tweets sobre el tema?")

print(tweet_handler.get_more_objetivity(table_type="hist",
                                        since=startDate, until=stopDate, img_src="result/more_objetivity.png"))

startDate = datetime.datetime(2023, 1, 20)
stopDate = datetime.datetime(2023, 3, 31)
print(f"Usando como muestra el periodo: \n inicio {startDate} fin: {stopDate} se espera un sentimiento: ",
      tweet_handler.media_probabilistica_sentimiento(since=startDate, until=stopDate))
