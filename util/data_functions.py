import string
import re

import emoji

import pandas as pd
import matplotlib.pyplot as plt


import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

from textblob import TextBlob
from collections import Counter

from wordcloud import WordCloud

from tweets.translate import TranslateGoogle


class DataAnalisis():

    def __init__(self) -> None:
        self.translator = TranslateGoogle()
        
        self.tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        self.stemmer = PorterStemmer()
        self.stopwords_english = set(stopwords.words('english'))


    def get_text_sentiment(self, text):

        # Analize
        sentiment = TextBlob(str(text)).sentiment

        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        return polarity, subjectivity

    def clean_tweet(self, tweet):

        tweet = str(tweet).strip()
        # Remove stock market tickers like $AAPL and $GOOG
        tweet = re.sub(r'\$\w+', '', tweet)

        # Remove retweet text "RT"
        tweet = re.sub(r'^RT[\s]+', '', tweet)

        # Remove hyperlinks
        tweet = re.sub(r'https?:\/\/\S+', '', tweet)

        # Remove hashtags
        # Only removing the hash # sign from the word
        tweet = re.sub(r'#', '', tweet)

        tweet = emoji.demojize(tweet)

        tweet = tweet.encode('ascii', 'ignore')

        tweet_tokens = self.tokenizer.tokenize(tweet)
        tweet_tokens = [self.stemmer.stem(w.lower()) for w in tweet_tokens if w.lower(
        ) not in self.stopwords_english and w.lower() not in string.punctuation]

        return ' '.join(tweet_tokens)

    def translate_content(self, content_list):
        return self.translator.async_translate(content_list)

    # Obtener las palabras más utilizadas en los tweets
    # Dibujar nube de palabras
    def get_most_used_words(self, content_list, cant, img_src):

        words = []

        for content in content_list:
            for text in content:
                for word in text.split(" "):
                    words.append(word)

        word_counts = Counter(words)
        top_words = word_counts.most_common(cant)

        words_cloud = {}
        for word_aux, frec_aux in top_words:
            words_cloud[word_aux] = frec_aux

        word_cloud = WordCloud(
            collocations=False, background_color="white").generate_from_frequencies(words_cloud)

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

    # Exclusive method of pandas
    def get_data_frecuency(self, dataframe, column, title, kind, img_src):

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

    def load_from_cvs(self, file_src):
        data = pd.read_csv(file_src)
        return data

    def load_from_json(self, file_src):
        data = pd.read_json(file_src)
        return data
