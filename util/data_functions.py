import string
import re
import unicodedata

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

        self.stemmer = PorterStemmer()
        self.stopwords_english = stopwords.words('english')

    def get_text_sentiment(self, text):

        # Analize
        sentiment = TextBlob(str(text)).sentiment

        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        return polarity, subjectivity

    def clean_tweet(self, tweet):
        """ 
        The regular expressions for removing stock market tickers,
          retweet text, hyperlinks, and hashtags can be combined into
            one expression using the pipe
              operator: r'\$?\w*|^RT[\s]+|https?:\/\/.*[\r\n]*|#'."""

        tweet = str(tweet)

        tweet = re.sub(r'\$?\w*|^RT[\s]+|https?:\/\/.*[\r\n]*|#', '', tweet)

        emoticon_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF\U0001F900-\U0001F9FF\U0001F1E6-\U0001F1FF\u0023-\u0039\u2000-\u206F\u20A0-\u20CF\u2100-\u214F\u2190-\u21FF\u2200-\u22FF\u2300-\u23FF\u2460-\u24FF\u25A0-\u25FF\u2600-\u26FF\u2700-\u27BF\u2B00-\u2BFF\u2900-\u297F\u3200-\u32FF\u1F910-\u1F96B\u1F980-\u1F991\u1F9C0-\u1F9C0]'

        tweet = re.sub(emoticon_pattern, '', tweet)

        tweet = unicodedata.normalize('NFD', tweet).encode('ASCII', 'ignore').decode('utf-8')

        ascii_pattern = r'[a-zA-Z]+'

        tweet = re.sub(ascii_pattern, '', tweet)       

        tokenizer = TweetTokenizer(
            preserve_case=False, strip_handles=True, reduce_len=True)
        tweet_tokens = tokenizer.tokenize(tweet)
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
