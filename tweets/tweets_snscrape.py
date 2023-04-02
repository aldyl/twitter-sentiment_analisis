
from snscrape.modules.twitter import TwitterSearchScraper

class SnscrapeTwiteer:
    def __init__(self) -> None:
        pass
        
    def get_by_user(self, user='AthemAl', cant=0):

        try:
            query_sn = enumerate(TwitterSearchScraper(
                f'from:{user}').get_items())
            print("Tweets recolectados")
        except:
            print("Some error in connection to twiter")

        return query_sn

        # COVID Vaccine since:2021-01-01 until:2021-05-31
    def get_by_query(self, query="Some", since='', until=''):

        try:
            query_sn = enumerate(TwitterSearchScraper(
                f'{query} since:{since}] until:{until}').get_items())
            print("Tweets recolectados")
        except:
            print("Some error in connection to twiter")

        return query_sn