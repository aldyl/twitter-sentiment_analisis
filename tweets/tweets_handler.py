
import string
import re

import pandas as pd
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from textblob import TextBlob
from collections import Counter

from tweets.translate import TranslateGoogle

from wordcloud import WordCloud

from model.mysql_connector import MysqlConnector
from tweets.tweets_snscrape import SnscrapeTwiteer


DEBUG = True


class Tweets:

    def __init__(self) -> None:

        self.translator = TranslateGoogle()
        self.sn_twitter = SnscrapeTwiteer()
        self.mysql_connector = MysqlConnector(
            user="twitter", password="password", host="localhost", database="tweets_db")

    def build_tweet_list(self, table="", query_result="", cant=100):

        tweet_list = []

        tweet_found = 0
        twwet_on_bd = 0

        for i, tweet in query_result:
            if i >= cant:  # max k number of tweets
                break

            tweet_found += 1

            # Sns scrape documentation tweet structure ID in twwet[0]
            if self.mysql_connector.tweet_en_bd(table=table, tweet_id=tweet[0]) is None:
                
                tweet_list = self.tweet_process(
                    tweet_list, tweet)
    
            else:
                twwet_on_bd += 1

        if DEBUG:
            print(f"Tweets scraper: found {tweet_found}, on bd: {twwet_on_bd}")

        return tweet_list

    def get_by_query(self, table="", query="", cant=100, since='', until=''):

        sn_twitter = self.sn_twitter.get_by_query(
            query=query,  since=since, until=until)

        tweet_list = self.build_tweet_list(
            table=table, query_result=sn_twitter, cant=cant)

        self.mysql_connector.create_tweet_table(table)

        self.mysql_connector.insert_tweet_on_table(
            table, tweets=tweet_list)
        
        self.mysql_connector.close()

        print("Tweets importados")

    def tweet_process(self, tweet_list, tweet):

        # Critical zone translate tweets to english.
        content_translated, languaje = self.translator.translate(
            tweet.renderedContent)
        # Time end slow

        # Clean tweets
        content = self.clean(
            content_translated, lang=languaje)

        # Impact value on public tweet algotithm.
        impact = int(tweet.retweetCount) + int(tweet.likeCount)

        # Sentiment Objetivity
        polarity, objetivity = self.get_tweet_sentiment(content)

        # Data Frame Key Id, Date, Content, Impact, Polarity, Objective
        tweet_list.append([tweet.id, tweet.date, content,
                          impact, polarity, objetivity])

        return tweet_list

    def clean(self, tweet, lang='spanish'):

        tokens = nltk.word_tokenize(tweet)

        # convertir a minúsculas
        tokens = [w.lower() for w in tokens]

        # prepare a regex para el filtrado de caracteres
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))

        # eliminar la puntuación de cada palabra
        stripped = [re_punc.sub('', w) for w in tokens]

        # eliminar los tokens restantes que no estén en orden alfabético
        words = [word for word in stripped if word.isalpha()]

        # filtrar las palabras de interrupción
        stop_words = set(stopwords.words(lang))
        words = [w for w in words if not w in stop_words]

        # derivado de las palabras a su base
        porter = PorterStemmer()
        words = [porter.stem(word) for word in words]

        return ' '.join(map(str, words))

    def get_tweet_sentiment(self, tweet):
        # Analizar el sentimiento de los tweet

        sentiment = TextBlob(str(tweet)).sentiment

        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        return polarity, subjectivity

    # Obtener las palabras más utilizadas en los tweets
    def get_most_used_words(self, content_tweets_list, cant, img_src):

        words = []

        for tweet in content_tweets_list:
            for text in tweet:
                for word in text.split(" "):
                    words.append(word)

        word_counts = Counter(words)
        top_words = word_counts.most_common(cant)

        cloud = {}
        for word_a, frec_a in top_words:
            cloud[word_a] = frec_a

        word_cloud = WordCloud(
            collocations=False, background_color="white").generate_from_frequencies(cloud)

        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(img_src)

        return top_words

    """"
    The kind of plot to produce:
    ‘line’ : line plot (default)
    ‘bar’ : vertical bar plot
    ‘barh’ : horizontal bar plot
    ‘hist’ : histogram
    ‘box’ : boxplot
    ‘kde’ : Kernel Density Estimation plot
    ‘density’ : same as ‘kde’
    ‘area’ : area plot
    ‘pie’ : pie plot
    ‘scatter’ : scatter plot (DataFrame only)
    ‘hexbin’ : hexbin plot (DataFrame only)
    """

    def get_tweet_data_frecuency(self, dataframe, column, title, kind, img_src):

        # Round data to 1 decimal
        for col in dataframe.columns:
            dataframe[col] = round(dataframe[col], 2)

        # Remove Outliers
        Q1 = dataframe.quantile(0.25)
        Q3 = dataframe.quantile(0.75)
        IQR = Q3-Q1
        dataframe = dataframe[~(
            (dataframe < (Q1-1.5 * IQR)) | (dataframe > (Q3 + 1.5 * IQR))).any(axis=1)]
        dataframe.shape

        # Count frecuency
        dataframe_df = dataframe.groupby(
            column).size().reset_index(name="counts")

        # Plot the frequency of each sentiment
        dataframe_df.plot(kind=kind, x="counts", y=column, color="blue")

        plt.title(column + " Frequency for " + title +
                  " Media estadistica: " + str(IQR[0]))
        plt.xlabel("Frequency")
        plt.ylabel(column)
        plt.savefig(img_src)

        return IQR

    def tweet_to_csv(self, tweets_list, file_src, columns=['Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ], ):

        tweets_df = pd.DataFrame(tweets_list, columns=columns)

        tweets_df.to_csv(file_src, sep=';', decimal=',')

        return tweets_df

    def tweet_to_json(self, tweets_list, file_src, columns=['Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ], ):

        tweets_df = pd.DataFrame(tweets_list, columns=columns)

        tweets_df.to_json(file_src)

        return tweets_df

    def load_from_cvs(self, file_src):
        data = pd.read_csv(file_src)
        return data

    def load_from_json(self, file_src):
        data = pd.read_json(file_src)
        return data
