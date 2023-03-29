#!/bin/python3

import tweepy

# Autenticación de la API de Twitter
CONSUMER_KEY = 'tu_consumer_key'
CONSUMER_SECRET = 'tu_consumer_secret'
ACCESS_TOKEN = 'tu_access_token'
ACCESS_TOKEN_SECRET = 'tu_access_token_secret'


class TwitterConnector:
    def __init__(self):

        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = tweepy.API(self.auth)

    def get_api(self):
        return self.api

    # Obtener los trending topics de México por defecto
    def get_trending_topic_for_woeid(self, woeid=23424900):
        return self.api.get_place_trends(woeid)

    def get_trends_names(self, woeid):
        for trend in self.get_trending_topic_for_woeid(woeid)[0]["trends"]:
            print(trend["name"])

    def get_relevant_tweets(self, search_sentence='evento deportivo', cant_results=100):
        # Obtener los tweets relevantes
        tweets = self.api.search_tweets(q=search_sentence, count=cant_results)
        return tweets
