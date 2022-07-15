from database.models import News
from database.core import db_session
from datetime import datetime, timedelta
from config.config import GROUP_EDIT_ID, GROUP_MAIN_ID
from .messenger import BaseNewsSender, EditingNewsSender


class NewsPublisher:

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def _get_news(start_date=None, end_date=None) -> list[News]:
        if not start_date:
            start_date = NewsPublisher.now()

        if not end_date:
            end_date = NewsPublisher.now() + timedelta(days=1)

        with db_session:
            nb_date = News.get_from_db_by_datetime(open_session=db_session,
                                                   start_date=start_date,
                                                   end_date=end_date)

        return nb_date

    @staticmethod
    def _prepare_news(news_list: list[News]):
        if news_list is None:
            return []
        return [BaseNewsSender(news) for news in news_list if not news.telegram_news_id]

    @staticmethod
    def _prepare_news_to_edit(news_list: list[News]):
        if news_list is None:
            return []
        return [EditingNewsSender(news) for news in news_list if not news.telegram_news_id_edit]

    @staticmethod
    async def publish_event(start_date=None, end_date=None, count: int = None):
        # get news from database
        raw_news = NewsPublisher._get_news(start_date=start_date, end_date=end_date)

        # prepare news to send
        prepared_news = NewsPublisher._prepare_news(news_list=raw_news)
        prepared_news_to_edit = NewsPublisher._prepare_news_to_edit(news_list=raw_news)

        # post news in main group
        # todonext only 1 post
        await BaseNewsSender.bulk_post_news(news_list=prepared_news, group_chat_id=GROUP_MAIN_ID, count=count)
        await EditingNewsSender.bulk_post_news(news_list=prepared_news_to_edit, group_chat_id=GROUP_EDIT_ID, count=count)
