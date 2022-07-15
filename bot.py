from icecream import ic

from controllers import handlers
from aiogram import executor
from config.bot_setup import dispatcher
from controllers.core.scrapper.scrapper import parse_news

if __name__ == '__main__':
    ic('parse starting')
    parse_news()
    handlers.setup(dispatcher)
    executor.start_polling(dispatcher, skip_updates=False)
