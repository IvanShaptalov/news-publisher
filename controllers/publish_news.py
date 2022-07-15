from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic

import config.config
from .core.news.publisher import NewsPublisher
from datetime import datetime, timedelta

from .core.scrapper.scrapper import parse_news


async def handle_post_news(message: types.Message, state: FSMContext):  # post
    if str(message.chat.id) != str(config.config.GROUP_EDIT_ID):
        ic('post not from edit group')
        return
    # news

    parse_news()

    await NewsPublisher.publish_event(start_date=datetime.now() - timedelta(days=2),
                                      end_date=datetime.now() + timedelta(days=1),
                                      count=1)
