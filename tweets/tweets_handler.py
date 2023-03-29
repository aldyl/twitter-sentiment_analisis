from collections import Counter
import string
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from textblob import TextBlob

class Tweets:
    def __init__(self) -> None:
        self.tweets = []

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
    
    def most_used_words(self, tweets, count=10):
        # Obtener las palabras más utilizadas en los tweets
        words = []
        for tweet in tweets:
            words += tweet.split()

        word_counts = Counter(words)
        top_words = word_counts.most_common(count)

        return top_words


    def get_tweet_sentiment(self, tweet):
        # Analizar el sentimiento de los tweet
 
        sentiment = TextBlob(str(tweet)).sentiment

        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        return polarity, subjectivity
        

