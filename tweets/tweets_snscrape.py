
from snscrape.modules.twitter import TwitterSearchScraper


class SnscrapeTwiteer:
    def __init__(self) -> None:
        pass

    def get_by_user(self, user):

        try:
            query_sn = enumerate(TwitterSearchScraper(
                f'from:{user}').get_items())

            print(f"SNScraper search user: {user}")
        except:
            print("Some error in connection to twiter")

        return query_sn

        # COVID Vaccine since:2021-01-01 until:2021-05-31
    def get_by_query(self, query, since, until):

        try:

            query_sn = enumerate(TwitterSearchScraper(
                query=f'{query} since:"{since}" until:"{until}"').get_items())

            print(f'{query} since:"{since}" until:"{until}"')

        except:
            print("Some error in connection to twiter")

        return query_sn
