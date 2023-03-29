
import pandas as pd
from tweets.tweets_handler import Tweets
from tweets.translate import Translate
from snscrape.modules.twitter import TwitterSearchScraper


class SnscrapeTwiteer:
    def __init__(self) -> None:
        self.translator = Translate()
        self.tweet_handler = Tweets()

    def get_by_user(self, user, cant):

        tweet_list = []

        try:
            query_sn = enumerate(TwitterSearchScraper(
                f'from:{user}').get_items())
            print("Tweets recolectados")
        except:
            print("Some error in connection to twiter")

        for i, tweet in query_sn:
            if i >= cant:  # max k number of tweets
                break

            tweet_list = self.tweet_process(tweet_list, tweet)

        return tweet_list

        # COVID Vaccine since:2021-01-01 until:2021-05-31
    def get_by_query(self, query, cant, since='', until=''):

        tweet_list = []

        try:
            query_sn = enumerate(TwitterSearchScraper(
                f'{query} since:{since}] until:{until}').get_items())
            print("Tweets recolectados")
        except:
            print("Some error in connection to twiter")

        for i, tweet in query_sn:
            if i >= cant:  # max k number of tweets
                break

            tweet_list = self.tweet_process(tweet_list, tweet)

        return tweet_list

    def tweet_process(self, tweet_list, tweet):

        # Translate tweets
        content_translated, languaje = self.translator.translate(
            tweet.renderedContent)

        # Clean tweets
        content = self.tweet_handler.clean(
            content_translated, lang=languaje)

        # Impact value
        impact = int(tweet.retweetCount) + int(tweet.likeCount)

        # Sentiment Objetivity
        polarity, objetivity = self.tweet_handler.get_tweet_sentiment(content)

        # Remove tweet without objetive
        if objetivity > 0.1:
            # Data Frame Key Id, Date, Content, Impact, Polarity, Objective
            tweet_list.append([tweet.id, tweet.date, content, impact, polarity, objetivity ])

        return tweet_list
    
    def get_most_used_words(self, tweets_list, cant):

        tweets_content_list = []

        for tweet in tweets_list:
            tweets_content_list.append(tweet[2])
     
        return self.tweet_handler.most_used_words(tweets_content_list, count=cant)


    def tweet_to_csv(self, tweets_list, file_src):

        tweets_df = pd.DataFrame(tweets_list, columns=[
                                 'Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ])
        tweets_df.to_csv(file_src, sep=';', decimal=',')

    def tweet_to_json(self, tweets_list,  file_src):

        tweets_df = pd.DataFrame(tweets_list, columns=[
                                 'Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ])
        tweets_df.to_json(file_src)

    def load_from_cvs(self, file_src):
        data = pd.read_csv(file_src)
        return data

    def load_from_json(self, file_src):
        data = pd.read_json(file_src)
        return data
