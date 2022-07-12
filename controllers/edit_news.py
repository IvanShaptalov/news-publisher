import logging

from aiogram import types
from icecream import ic

from config import text_util
from config.config import START


async def handle_start(message: types.Message, state=None):
    ic(START)
    ic(message.chat.id)
    await message.reply(text_util.MAIN_MENU_OPENED)
    if state:
        await state.finish()
        logging.info('leave chat, chat state finish')


# todonext create news handling: delete, edit

async def handle_delete_callback():
    pass


async def handle_edit_callback():
    pass


async def handle_text_entered_reply(message: types.Message, state=None):
    pass


async def handle_save_reply(message: types.Message, state=None):
    pass


async def handle_cancel_reply(message: types.Message, state=None):
    pass
