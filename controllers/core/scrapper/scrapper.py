import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from babel.dates import parse_date
import requests
from bs4 import BeautifulSoup, Tag
from requests import Response

from config.config import ScrapURLS as SL
from database.core import db_session
from database.models import News


class Parser(ABC):

    def __init__(self, link=None):
        self._page: Response = None
        self.main_link = link

    @abstractmethod
    def get_news(self):
        pass

    @abstractmethod
    def save_news(self, pnews=None):
        pass

    @staticmethod
    @abstractmethod
    def date_to_str(time: datetime, time_format: str, lang: str = None):
        pass

    @staticmethod
    @abstractmethod
    def date_from_str(str_date, time_format: str, lang: str = None):
        pass

    def _get_html_doc(self, url) -> Response:
        self._page = requests.get(url)
        return self._page

    def _soup_from_page(self, url=None) -> BeautifulSoup:
        if self._page is None:
            assert url is not None
            self._get_html_doc(url)
        return BeautifulSoup(self._page.text, 'html.parser')


class OsvitaParser(Parser):
    @staticmethod
    def date_to_str(time: datetime, time_format: str, lang: str = None):
        pass

    @staticmethod
    def date_from_str(str_date, time_format: str, lang: str = None):
        pass

    def __init__(self):
        super().__init__(link=SL.OSVITA_URL)
        self._soup = self._soup_from_page(self.main_link)
        self.news_list: list = []

    def get_news(self):
        def get_time(iterate_div) -> datetime:
            time = iterate_div.find('span', attrs={'class': 'bdate'})
            if isinstance(time, Tag):
                if time.text:
                    return parse_date(time.text)
            return None

        def get_link(iterate_div):
            link = iterate_div.find('a')
            if isinstance(link, Tag):
                href = link.get('href')
                if href:
                    return self.main_link + href
            return None

        def get_text(iterate_div):
            tag_text = iterate_div.find('a')
            if tag_text and tag_text.text:
                return NusOrgUaParser.prepare_text(tag_text.text)
            return None

        def get_title(iterate_div):
            raw_link = iterate_div.find('a')
            if isinstance(raw_link, Tag):
                title = raw_link.get('title', None)
                if title:
                    return NusOrgUaParser.prepare_text(title)
            return None

        result = []
        table = self._soup.find('table', attrs={'class': ["gtab", "list"]})
        trs = table.find_all('tr')
        if trs:
            for div in trs:
                news_item = None
                if isinstance(div, Tag):
                    news_item = {
                        'time': get_time(div),
                        'href': get_link(div),
                        'text': "{0}\n{1}".format(get_title(div),
                                                  get_text(div)),
                        'source_title': 'osvita.ua',
                        'source_link': self.main_link,
                    }

                if news_item.get('time', None) \
                        and news_item.get('href', None) \
                        and news_item.get('text', None):
                    result.append(news_item)
        if result:
            self.news_list = result
        return result

    @staticmethod
    def prepare_text(raw_text: str):
        return raw_text.replace('  ', '').replace('\n', '')

    def save_news(self, pnews=None):
        r_news = pnews if pnews else self.news_list
        with db_session:
            for news_item in r_news:
                news_item = News(news_id=str(uuid.uuid4()),
                                 text=news_item.get('text'),
                                 source_title=news_item.get('source_title'),
                                 source_link=news_item.get('source_link'),
                                 news_link=news_item.get('href'),
                                 date=news_item.get('time'),
                                 telegram_news_id='')
                news_item.save(db_session)
        print('saved')
        return r_news


class NusOrgUaParser(Parser):
    @staticmethod
    def date_to_str(time: datetime, time_format: str, lang: str = None):
        pass

    @staticmethod
    def date_from_str(str_date, time_format: str, lang: str = None):
        pass

    def __init__(self):
        super().__init__(link=SL.NUSORGUA_URL)
        self._soup = self._soup_from_page(self.main_link)
        self.news_list: list = []
        self.time_table = {'січня': '1',
                           'лютого': '2',
                           'березня': '3',
                           'квітня': '4',
                           'травня': '5',
                           'червня': '6',
                           'липня': '7',
                           'серпня': '8',
                           'вересня': '9',
                           'жовтня': '10',
                           'листопада': '11',
                           'грудня': '12'}

    def get_news(self):
        def get_time(iterate_div):
            p_tag = iterate_div.find('p', attrs={'class': 'news_list-item-date'})
            if p_tag and p_tag.text:
                return from_str_to_date(p_tag.text)
            return None

        def from_str_to_date(str_date: str) -> datetime:
            for k, v in self.time_table.items():
                if k in str_date.lower():
                    res_str_date = str_date.lower().replace(k, v).replace(' ', '.')
                    return parse_date(res_str_date)

        def get_link(iterate_div):
            a_tag = iterate_div.find('a', attrs={'class': 'head'})
            if a_tag and a_tag.get('href', None):
                return a_tag.get('href')

            return None

        def get_text(iterate_div):
            a_tag = iterate_div.find('a', attrs={'class': 'head'})
            if a_tag and a_tag.text:
                return NusOrgUaParser.prepare_text(a_tag.text)

            return None

        result = []
        divs = self._soup.find_all('div', attrs={'class': "news_list-item"})

        if divs:
            for div in divs:
                news_item = None
                if isinstance(div, Tag):
                    news_item = {
                        'time': get_time(div),
                        'href': get_link(div),
                        'text': get_text(div),
                        'source_title': 'nus.org.ua',
                        'source_link': self.main_link,

                    }

                if news_item.get('time', None) and news_item.get('href', None) and news_item.get('text', None):
                    result.append(news_item)
        if result:
            self.news_list = result
        return result

    @staticmethod
    def prepare_text(raw_text: str):
        return raw_text.replace('  ', '').replace('\n', '')

    def save_news(self, pnews=None):
        r_news = pnews if pnews else self.news_list
        with db_session:
            for news_item in r_news:
                news_item = News(news_id=str(uuid.uuid4()),
                                 text=news_item.get('text'),
                                 source_title=news_item.get('source_title'),
                                 source_link=news_item.get('source_link'),
                                 news_link=news_item.get('href'),
                                 date=news_item.get('time'),
                                 telegram_news_id='')
                news_item.save(db_session)
        print('saved')
        return r_news
