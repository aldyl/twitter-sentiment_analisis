import string
import re
import unicodedata

import pandas as pd
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TweetTokenizer

from textblob import TextBlob
from collections import Counter

from wordcloud import WordCloud

from tweets.translate import TranslateGoogle

class DataAnalisis():

    def __init__(self) -> None:
        self.translator = TranslateGoogle()

    def get_text_sentiment(self, text):

        # Analize
        sentiment = TextBlob(str(text)).sentiment

        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        return polarity, subjectivity

    def clean_content(self, tweet, lang='spanish'):

        # remove stock market tickers like $GE
        tweet = re.sub(r'\$\w*', '', str(tweet))
        # remove old style retweet text "RT"
        tweet = re.sub(r'^RT[\s]+', '', str(tweet))
        # remove hyperlinks
        tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', str(tweet))
        # remove hashtags
        # only removing the hash # sign from the word
        tweet = re.sub(r'#', '', str(tweet))
        # tokenize tweets
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
        tweet_tokens = tokenizer.tokenize(tweet)
        # convertir a minúsculas
        tweet_tokens = [w.lower() for w in tweet_tokens]
        
        stemmer = PorterStemmer()
        stopwords_english = stopwords.words(lang)
        
        tweets_clean = []
        for word in tweet_tokens:
            if (word not in stopwords_english and  # remove stopwords
                    word not in string.punctuation):  # remove punctuation
                # tweets_clean.append(word)
                stem_word = stemmer.stem(word)  # stemming word
                tweets_clean.append(stem_word)

        return " ".join(tweets_clean)
        #return ' '.join(map(str, words))

    def content_prepare(self, text):

        # Critical zone translate tweets to english.
        content_translated, languaje = self.translator.translate(
            text)

        # TODO Some tweaks to translate are run async functions on python.

        # Clean tweets
        content = self.clean_content(
            content_translated, lang=languaje)

        return content

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
