import requests
from typing import Dict, List
from .feed import NewsFeed, NewsItem
from .utils import decode_html_body


class NewsScraper:
    """
    Base class for news scrapers. Common scraping/news feed functionality used
    across multiple counties should be implemented here. This class should be
    inherited and never used directly.

    To run a scraper, call the `get_news()` class method:
    >>> class SomeCounty(NewsScraper):
    >>>     ...
    >>> news_feed = SomeCounty.get_news()

    Classes inheriting from this should set ``URL`` to the URL from which
    scraping should start, then implement `parse_page()`, which returns a list
    of news items given some HTML.
    """
    FEED_INFO: Dict = {}
    URL = ''

    def create_feed(self) -> NewsFeed:
        return NewsFeed(**self.FEED_INFO)

    def scrape(self) -> NewsFeed:
        """
        Create and return a news feed.

        Returns
        -------
        list of dict

        Examples
        --------
        >>> scraper = SanFranciscoNews()
        >>> scraper.scrape()
        [{'url': 'https://sf.gov/news/expansion-coronavirus-testing-all-essential-workers-sf',
          'text': 'Expansion of coronavirus testing for all essential workers in SF',
          'date': '2020-04-23T04:11:56Z'}]
        """
        feed = self.create_feed()
        html = self.load_html(self.URL)
        news = self.parse_page(html, self.URL)
        feed.append(*news)
        return feed

    def load_html(self, url: str) -> str:
        response = requests.get(self.URL)
        response.raise_for_status()
        return decode_html_body(response)

    def parse_page(self, html: str, url: str) -> List[NewsItem]:
        raise NotImplementedError()

    @classmethod
    def get_news(cls) -> NewsFeed:
        instance = cls()
        return instance.scrape()
