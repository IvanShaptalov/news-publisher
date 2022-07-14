from icecream import ic

from controllers import handlers
from aiogram import executor
from config.bot_setup import dispatcher
from controllers.core.scrapper.scrapper import NusOrgUaParser, OsvitaParser


def parse_news():
    try:
        nus = NusOrgUaParser()
        nus.get_news()
        nus.save_news()
        ic('nus news saved')

        osvita = OsvitaParser()
        osvita.get_news()
        osvita.save_news()
        ic('osvita news saved')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    ic('parse starting')
    parse_news()
    handlers.setup(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True)
