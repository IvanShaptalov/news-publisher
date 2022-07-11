from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic

import config.config
from .core.news.publisher import NewsPublisher
from datetime import datetime, timedelta


async def handle_post_news(message: types.Message, state: FSMContext):  # post news
    ic(config.config.POST)
    await NewsPublisher.publish_event(start_date=datetime.now() - timedelta(days=4),
                                      end_date=datetime.now() - timedelta(days=3))
