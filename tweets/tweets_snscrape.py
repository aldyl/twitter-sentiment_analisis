
from snscrape.modules.twitter import TwitterSearchScraper
from tweets.tweets_handler import Tweets

class SnscrapeTwiteer:
    def __init__(self) -> None:
        
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

            tweet_list = self.tweet_handler.tweet_process(tweet_list, tweet)

        
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

            tweet_list = self.tweet_handler.tweet_process(tweet_list, tweet)

        return tweet_list

