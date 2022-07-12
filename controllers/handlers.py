from aiogram.dispatcher.filters import Text

from config import config
from states.service import StatesGroup
from . import edit_news, publish_news
from aiogram import Dispatcher
from config import text_util


def setup(dp: Dispatcher):
    # region start feature
    dp.register_message_handler(edit_news.handle_start, Text(equals=config.START), state='*')
    # endregion start feature

    # region news posting
    dp.register_message_handler(publish_news.handle_post_news, Text(equals=config.POST), state='*')

    # endregion posting

    # region text editing
    dp.register_callback_query_handler(edit_news.handle_edit_callback,
                                       lambda callback: text_util.EDIT_POST in callback.data, state='*')

    dp.register_callback_query_handler(edit_news.handle_delete_callback,
                                       lambda callback: text_util.DELETE_POST in callback.data,
                                       state='*')

    dp.register_message_handler(edit_news.handle_text_entered_reply, content_types=['text'], state=StatesGroup.edit_state)

    dp.register_message_handler(edit_news.handle_cancel_reply, Text(equals=text_util.CANCEL_EDITING), state=StatesGroup.text_entered_state)

    dp.register_message_handler(edit_news.handle_save_reply, Text(equals=text_util.SAVE_POST), state=StatesGroup.text_entered_state)
    # endregion text editing

