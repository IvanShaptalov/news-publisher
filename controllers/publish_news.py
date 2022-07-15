from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic

import config.config
from .core.news.publisher import NewsPublisher
from datetime import datetime, timedelta

from .core.scrapper.scrapper import parse_news

counter = 0


async def handle_post_news(message: types.Message, state: FSMContext):  # post
    if str(message.chat.id) != str(config.config.GROUP_EDIT_ID):
        ic('post not from edit group')
        return
    # news
    global counter
    ic(config.config.POST)
    if counter == 3:
        counter = 0
        parse_news()
        ic('parse from counter')
    counter += 1
    await NewsPublisher.publish_event(start_date=datetime.now() - timedelta(days=2),
                                      end_date=datetime.now() + timedelta(days=1),
                                      count=2)
