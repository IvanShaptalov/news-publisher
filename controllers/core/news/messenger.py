from config.bot_setup import bot
from database.models import News


class BaseNewsSender:
    bot = bot

    def __init__(self, news: [dict | News]):
        if isinstance(news, dict):
            self.news_id = news.get('news_id', None)
            self.text = news.get('text', None)
            self.source_title = news.get('source_title', None)
            self.source_link = news.get('source_link', None)
            self.news_link = news.get('news_link', None)
            self.date = news.get('date', None)
            self.telegram_news_id = news.get('telegram_news_id', None)

        elif isinstance(news, News):
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
        return 'prepared text: {}\n' \
               'date: {}'.format(self.text, self.date.day
                                 )

    async def post_news(self, group_chat_id):
        await bot.send_message(chat_id=group_chat_id,
                               text=self.prepare_text())
        return True

    @staticmethod
    async def bulk_post_news(news_list: list['BaseNewsSender'], group_chat_id):
        if news_list is None:
            print('empty')
            return False
        for news_item in news_list:
            await news_item.post_news(group_chat_id=group_chat_id)

        return True
