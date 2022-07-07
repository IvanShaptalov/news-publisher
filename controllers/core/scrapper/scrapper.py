from datetime import datetime
from abc import ABC, abstractmethod
from pprint import pprint
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag
from requests import Response

import config.config
from config.config import ScrapURLS as SL


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
    def time_formatter(time: datetime, time_format: str):
        fsd = time.strftime(time_format) if isinstance(time, datetime) else ''  # formatted start date
        return fsd

    def _get_html_doc(self, url) -> Response:
        self._page = requests.get(url)
        return self._page

    def _soup_from_page(self, url=None) -> BeautifulSoup:
        if self._page is None:
            assert url is not None
            self._get_html_doc(url)
        return BeautifulSoup(self._page.text, 'html.parser')

    # region to realize
    #
    # def get_title(self) -> str:
    #     search_area = self.get_div_content(1)
    #     if search_area and search_area.contents:
    #         first_s = search_area.contents[0]
    #         script = first_s.contents[0]
    #         if isinstance(script, bs4.element.Script):
    #             str_script = script.__str__()
    #             title = self.get_value_from_attr_name(src=str_script, attr_key=["offers", "seller", "name"])
    #             return title
    #     return ''
    #
    # def get_city(self):
    #     regio = self.soup.find_all('span', attrs={'class': "companyLocation__region--1zzc4"})
    #
    #     if len(region) > 0 and region[0].text:
    #         city = region[0].text
    #         return city
    #
    # def get_phone(self):
    #     pre_script = self.soup.find_all('script', attrs={'type': 'application/javascript'})
    #     if len(pre_script) > 0 and pre_script[0].contents:
    #         if len(pre_script[0].contents) > 0 and pre_script[0].contents[0]:
    #             script = pre_script[0].contents[0]
    #             if isinstance(script, bs4.Script):
    #                 result = self.get_value_with_algorithm(script, "number")
    #                 phone = result
    #                 return phone
    #
    # def get_seller_link(self):
    #     search_area = self.get_div_content(1)
    #     if search_area and search_area.contents:
    #         first_s = search_area.contents[0]
    #         script = first_s.contents[0]
    #         if isinstance(script, bs4.element.Script):
    #             str_script = script.__str__()
    #             seller_link = self.get_value_from_attr_name(src=str_script, attr_key=["url"])
    #             return seller_link
    #
    # def get_info(self):
    #     title = self.get_title()
    #     city = self.get_city()
    #     type = 'none'
    #     phone = self.get_phone()
    #     seller_link = self.get_seller_link()
    #     return title, city, type, phone, seller_link
    #
    # @staticmethod
    # def get_value_from_attr_name(src, attr_key: list):
    #     """@:param src = data to json convert
    #     @:param attr_key = max deep = 5"""
    #     step_count = len(attr_key)
    #     data = json.loads(src)
    #     result = Nonelinks = soup.flinks = soup.find_all('a', attrs={'class': 'ek-link ek-link_blackhole_full-hover'})ind_all('a', attrs={'class': 'ek-link ek-link_blackhole_full-hover'})
    #     if step_count == 1:
    #         result = data[attr_key[0]]
    #     if step_count == 2:
    #         result = data[attr_key[0]][attr_key[1]]
    #     if step_count == 3:
    #         result = data[attr_key[0]][attr_key[1]][attr_key[2]]
    #     if step_count == 4:
    #         result = data[attr_key[0]][attr_key[1]][attr_key[2]][attr_key[3]]
    #     if step_count == 5:
    #         result = data[attr_key[0]][attr_key[1]][attr_key[2]][attr_key[3]][attr_key[4]]
    #     return result
    #
    # def get_div_content(self, index):
    #     divs = None
    #     try:
    #         divs = self.soup.find_all('div', attrs={'class': "basePage__content--3L2HZ"})
    #     except Exception as e:
    #         ic(type(e), e)
    #     if divs and len(divs) >= index:
    #         div = divs[0]
    #         if div and div.contents:
    #             return div.contents[0]
    #
    # @staticmethod
    # def get_value_with_algorithm(src: str, key):
    #     num_index = src.index(key)
    #
    #     if num_index > 0:
    #         src = src[num_index::]
    #         quote_index = src.index("\"")
    #         src = src[quote_index + 1::]
    #         quote_index = src.index("\"")
    #         src = src[quote_index + 1::]
    #         last_quote_index = src.index("\"")
    #         src = src[quote_index:last_quote_index]
    #         value = src
    #         return value


# endregion to realize


class OsvitaParser(Parser):
    def __init__(self):
        super().__init__(link=SL.OSVITA_URL)
        self._soup = self._soup_from_page(self.main_link)
        self.news_list: list = []

    def get_news(self):
        def get_time(iterate_div):
            time = iterate_div.find('span', attrs={'class': 'bdate'})
            if isinstance(time, Tag):
                if time.text:
                    return time.text
            # todo convert to datetime
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

                    }

                if news_item.get('time', None) \
                        and news_item.get('href', None) \
                        and news_item.get('text', None) \
                        and news_item.get('title', None):
                    result.append(news_item)
        if result:
            self.news_list = result
        return result

    @staticmethod
    def prepare_text(raw_text: str):
        return raw_text.replace('  ', '').replace('\n', '')

    def save_news(self, pnews=None):
        r_news = pnews if pnews else self.news_list

        pprint(r_news)
        print('saved')


class NusOrgUaParser(Parser):
    def __init__(self):
        super().__init__(link=SL.NUSORGUA_URL)
        self._soup = self._soup_from_page(self.main_link)
        self.news_list: list = []

    def get_news(self):
        def get_time(iterate_div):
            p_tag = iterate_div.find('p', attrs={'class': 'news_list-item-date'})
            if p_tag and p_tag.text:
                return p_tag.text

            return None

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
                        'text': get_text(div)
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

        pprint(r_news)
        print('saved')


if __name__ == '__main__':
    nus = NusOrgUaParser()
    news = nus.get_news()
    nus.save_news()

    osvita = OsvitaParser()
    news = osvita.get_news()
    osvita.save_news()
