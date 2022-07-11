import logging

from aiogram import types
from icecream import ic

from config import text_util
from config.config import START
import utils


async def handle_start(message: types.Message, state=None):
    ic(START)
    text = utils.get_full_user_name(message)

    await message.reply(text_util.MAIN_MENU_OPENED.format(text))
    if state:
        await state.finish()
        logging.info('leave chat, chat state finish')
