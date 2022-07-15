from aiogram.types import ParseMode

import config.config
import keyboards
from config import text_util
from config.bot_setup import bot
from database.core import db_session
from database.models import News


class BaseNewsSender:
    bot = bot

    def __init__(self, news: News):
        if news is not None:
            assert isinstance(news, News)
            self.news = news

            self.news_id = news.news_id
            self.text = news.text
            self.source_title = news.source_title
            self.source_link = news.source_link
            self.news_link = news.news_link
            self.date = news.date
            self.telegram_news_id = news.telegram_news_id

            self.prepared_text = self.prepare_text()

    def prepare_text(self):
        print(self.telegram_news_id)
        return '{0}\n\n' \
               '{1}\n' \
               '{2}\n\n' \
               '<a href="{3}">{4}</a> \n'.format(self.source_title,
                                                 self.date.strftime(config.config.TIME_FORMAT),
                                                 self.text,
                                                 self.news_link,
                                                 text_util.SOURCE_LINK)

    async def post_news(self, group_chat_id):
        message = await bot.send_message(chat_id=group_chat_id,
                                         text=self.prepare_text(),
                                         parse_mode=ParseMode.HTML)

        with db_session:
            self.news.telegram_news_id = message.message_id
            self.news.save(db_session,
                           identifier_to_value=[News.news_id == self.news.news_id])
        return True

    @staticmethod
    async def bulk_post_news(news_list: list['BaseNewsSender'], group_chat_id, count: int = 1):
        if news_list is None:
            print('empty')
            return False

        for index, news_item in enumerate(news_list):
            if index == count:
                break
            if isinstance(news_item, BaseNewsSender) or isinstance(news_item, EditingNewsSender):
                await news_item.post_news(group_chat_id=group_chat_id)

        return True


class EditingNewsSender(BaseNewsSender):
    def __init__(self, news: [News]):
        super().__init__(news)

    def prepare_text(self):
        print(self.telegram_news_id)
        return '*POST TO EDITING*\n{0}\n\n' \
               '{1}\n' \
               '{2}\n\n' \
               '<a href="{3}">{4}</a> \n'.format(self.source_title,
                                                 self.date.strftime(config.config.TIME_FORMAT),
                                                 self.text,
                                                 self.news_link,
                                                 text_util.SOURCE_LINK)

    async def post_news(self, group_chat_id):
        message = await bot.send_message(chat_id=group_chat_id,
                                         text=self.prepare_text(),
                                         reply_markup=keyboards.inline.editing_post_inline_keyboard(self.news_id),
                                         parse_mode=ParseMode.HTML)

        with db_session:
            self.news.telegram_news_id_edit = message.message_id
            self.news.save(db_session,
                           identifier_to_value=[News.news_id == self.news.news_id])
        return True
