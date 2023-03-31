
import string
import re
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from textblob import TextBlob
from collections import Counter

from tweets.translate import TranslateGoogle

class Tweets:

    def __init__(self) -> None:

        self.translator = TranslateGoogle()

    def tweet_process(self, tweet_list, tweet):

        # Critical zone translate tweets to english.
        content_translated, languaje = self.translator.translate(
            tweet.renderedContent)
        # Time end slow
        
        # Clean tweets
        content = self.clean(
            content_translated, lang=languaje)

        # Impact value
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
    def get_most_used_words(self, tweets_list, cant):
        words = []

        for tweet in tweets_list:

            words += tweet[2].split()

        word_counts = Counter(words)
        top_words = word_counts.most_common(cant)

        return top_words
    

    def  get_tweet_frecuency(self, tweets_list):

        sentiments = []

        for tweet in tweets_list:

            sentiments += tweet[4].split()
        
        # Calcular la frecuencia del sentimiento de los tweets
        frecuencias = nltk.FreqDist(sentiments)

        # Mostrar los resultados
        for sentimiento, frecuencia in frecuencias.items():
            print(f"{sentimiento}: {frecuencia/len(sentiments)}")

    


    def tweet_to_csv(self, tweets_list, file_src):

        tweets_df = pd.DataFrame(tweets_list, columns=[
                                 'Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ])
        tweets_df.to_csv(file_src, sep=';', decimal=',')

    def tweet_to_json(self, tweets_list, file_src, columns=['Id', 'Date', 'Content', 'Impact', 'Polarity', 'Objetivity', ], ):

        tweets_df = pd.DataFrame(tweets_list, columns)
        tweets_df.to_json(file_src)

    def load_from_cvs(self, file_src):
        data = pd.read_csv(file_src)
        return data

    def load_from_json(self, file_src):
        data = pd.read_json(file_src)
        return data
