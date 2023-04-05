
from model.mysql_connector import MysqlConnector
from tweets.tweets_snscrape import SnscrapeTwiteer
from util.data_functions import DataAnalisis
import pandas as pd
import numpy as np


DEBUG = False


class Tweets:

    def __init__(self, table):

        self.data_analisis = DataAnalisis()

        self.sn_twitter = SnscrapeTwiteer()

        self.mysql_connector = MysqlConnector(
            user="twitter", password="password",
            host="localhost", database="tweets_bd")

        self.table = table

    def load_internet_data(self, query, max_retrieve_tweets, since, until, max_descargas):
        
        print("Módulo de descarga de tweets")
        print(f'#{query} since:"{since}" until:"{until}"')

        parte = int(max_retrieve_tweets / 2)

        while parte > max_descargas:
            parte = int(parte / 2)

        cant_init = 0
        delta = parte

        while True:
            if parte > max_retrieve_tweets:
                break

            # Avoid memory overleak
            self.get_by_query(query=query, cant=parte, cant_init=cant_init,
                              since=since, until=until)
            cant_init = parte
            parte += delta

    def tweet_process(self, tweet_list, tweet):

        content = self.data_analisis.content_prepare(tweet.renderedContent)

        # Impact value on public tweet algorithm.
        # Is used to valorate

        impact = int(tweet.retweetCount) + int(tweet.likeCount)

        # Sentiment Objetivity
        polarity, objetivity = self.data_analisis.get_text_sentiment(content)

        # Data Frame Key Id, Date, Content, Impact, Polarity, Objective
        tweet_list.append([tweet.id, tweet.date, content,
                          impact, polarity, objetivity])

        return tweet_list

    def build_tweet_list(self, query_result, cant, cant_init):

        tweet_list = []

        tweet_process = 0
        tweet_on_bd = cant_init

        print_info = False

        for i, tweet in query_result:

            if print_info:
                print(
                f"descargados: {tweet_process}, on database: {tweet_on_bd} Total: {tweet_process+tweet_on_bd}")

            if i >= cant:  # max k number of tweets
                break

            if i <=cant_init:

                print_info = True

            else:

                if DEBUG:
                    print(i, cant, tweet)

                # Sns scrape documentation tweet structure ID

                out = self.mysql_connector.id_on_table_bd(
                    table=self.table, id=tweet.id)

                if out is None:

                    tweet_list = self.tweet_process(tweet_list, tweet)
                    tweet_process += 1

                else:

                    tweet_on_bd += 1

        return tweet_list

    def get_by_query(self, query, cant, cant_init, since='', until=''):

        sn_twitter = self.sn_twitter.get_by_query(
            query=query,  since=since, until=until)

        self.mysql_connector.create_tweet_table(self.table)

        tweet_list = self.build_tweet_list(
            query_result=sn_twitter, cant=cant, cant_init=cant_init)

        if DEBUG:
            print(f"Resultados en memoria {len(tweet_list)}")

        self.mysql_connector.insert_tweet_on_table(
            self.table, tweets=tweet_list)

    # (Id, Date, Content, Impact, Polarity, Objective)

    def get_tweet_timelapse_bd(self, columns='*', since='', until='') -> list:

        return self.mysql_connector.get_timelapse_bd(table=self.table, columns=columns,
                                                     since=since, until=until)

    def get_most_used_words(self, since, until, cant, img_src):

        columns_aux = 'Content'

        content_list = self.get_tweet_timelapse_bd(
            columns=columns_aux, since=since, until=until)

        return self.data_analisis.get_most_used_words(content_list, cant, img_src)

    def get_more_intense_sentiment(self, table_type="bar", since='', until='', img_src=''):

        columns_aux = 'Polarity'

        content_list = self.get_tweet_timelapse_bd(
            columns=columns_aux, since=since, until=until)

        tweet_df = self.tweet_to_json(
            content_list, "result/polarity.json", columns=[columns_aux])

        result = self.data_analisis.get_data_frecuency(
            tweet_df, columns_aux, self.table, table_type, img_src)

        if result[0] > 0.05:
            return "Positive"
        elif result[0] < -0.05:
            return "Negative"
        else:
            return "Neutral"

    def get_more_objetivity(self, table_type="bar", since='', until='', img_src=''):

        columns_aux = 'Objective'

        content_list = self.get_tweet_timelapse_bd(
            columns=columns_aux, since=since, until=until)

        tweet_df = self.tweet_to_json(
            content_list, "result/objetive.json", columns=[columns_aux])

        result = self.data_analisis.get_data_frecuency(
            tweet_df, columns_aux, self.table, table_type, img_src)

        if result[0] > 0.5:
            return "Objetivo"
        else:
            return "No Objetivos"

    def media_probabilistica_sentimiento(self, since='', until=''):

        columns_aux = 'Polarity, Impact'

        content_list = self.get_tweet_timelapse_bd(
            columns=columns_aux, since=since, until=until)

        polarity = []
        impact = []

        for n_tuple in content_list:
            polarity.append(n_tuple[0])
            impact.append(n_tuple[1] + 1)

        datos = np.array(polarity)

        probabilidades = np.array(impact)

        result = np.sum(datos * probabilidades) / sum(probabilidades)

        if result > 0.05:
            return "Positive"
        elif result > 0.01 and result < 0.05:
            return "Almost positive"
        elif result < -0.05:
            return "Negative"
        elif result < -0.01 and result > -0.05:
            return "Almost positive"
        else:
            return "Neutral"

    def tweet_to_csv(self, tweets_list, file_src, columns=['Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ], ):

        tweets_df = pd.DataFrame(tweets_list, columns=columns)

        tweets_df.to_csv(file_src, sep=';', decimal=',')

        return tweets_df

    def tweet_to_json(self, tweets_list, file_src, columns=['Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ], ):

        tweets_df = pd.DataFrame(tweets_list, columns=columns)

        tweets_df.to_json(file_src)

        return tweets_df
