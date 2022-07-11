from aiogram.dispatcher.filters import Text

from config import config
from . import edit_news, publish_news
from aiogram import Dispatcher


def setup(dp: Dispatcher):
    # in-chat futures
    dp.register_message_handler(edit_news.handle_start, Text(equals=config.START), state='*')

    dp.register_message_handler(publish_news.handle_post_news, Text(equals=config.POST), state='*')

    # dp.register_callback_query_handler(edit_news.show_event,
    #                                    lambda callback: config.SHOW_EVENT_MARKER in callback.data, state='*')
    #
    # dp.register_callback_query_handler(edit_news.connect_to_chat,
    #                                    lambda callback: config.CONNECT_TO_CHAT in callback.data,
    #                                    state='*')
    #
    # # exit from chat
    # dp.register_message_handler(edit_news.leave_chat, Text(equals=config.EXIT_FROM_CHAT), state='*')
    #
    # # chat
    # # chat content sending
    # dp.register_message_handler(publish_news.send_text_message, content_types=['text'], state=StatesGroup.in_chat)
    # dp.register_message_handler(publish_news.send_location, content_types=['location'], state=StatesGroup.in_chat)
    # dp.register_message_handler(publish_news.send_sticker, content_types=['sticker'], state=StatesGroup.in_chat)
    # dp.register_message_handler(publish_news.send_photo, content_types=['photo'], state=StatesGroup.in_chat)
    # dp.register_message_handler(publish_news.send_animation, content_types=['animation'], state=StatesGroup.in_chat)
    # dp.register_message_handler(publish_news.send_audio, content_types=['audio'], state=StatesGroup.in_chat)
    # dp.register_message_handler(publish_news.send_video, content_types=['video'], state=StatesGroup.in_chat)
    # dp.register_message_handler(publish_news.send_voice, content_types=['voice'], state=StatesGroup.in_chat)
    # service_bot

