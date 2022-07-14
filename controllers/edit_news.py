import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic

import config.config
import keyboards.reply
import utils
from config import text_util
from config.bot_setup import bot
from config.config import START
from database.core import db_session
from database.models import News
from states.service import StatesGroup


async def handle_start(message: types.Message, state=None):
    if state:
        await state.finish()
    ic(START)
    ic(message.chat.id)
    await message.reply(text_util.MAIN_MENU_OPENED)
    if state:
        await state.finish()
        logging.info('leave chat, chat state finish')


async def handle_delete_callback(callback: types.CallbackQuery, state: FSMContext):
    if state:
        await state.finish()
    id = utils.get_id_from_data(callback.data, 1)
    if id == 'button expired':
        await callback.message.reply(text=id)
        return
    with db_session:
        post = News.get_from_db(news_id=id, open_session=db_session)
        if isinstance(post, News):
            if post.telegram_news_id:
                await post.delete_message(message_id=post.telegram_news_id, chat_id=config.config.GROUP_MAIN_ID,
                                          bot=bot)

            if post.telegram_news_id_edit:
                await post.delete_message(message_id=post.telegram_news_id_edit, chat_id=config.config.GROUP_EDIT_ID,
                                          bot=bot)


async def handle_edit_callback(callback: types.CallbackQuery, state: FSMContext):
    await StatesGroup.text_entered_state.set()

    id = utils.get_id_from_data(callback.data, 1)
    await state.update_data(id=id)
    if id == 'button expired':
        await callback.message.reply(text=id)
        return
    await bot.send_message(chat_id=callback.message.chat.id,
                           text='enter text to editing')


async def handle_text_entered_reply(message: types.Message, state: FSMContext):
    if message.text.lower() != 'save':
        await StatesGroup.text_entered_state.set()
        await state.update_data(text=message.text)

        await bot.send_message(chat_id=message.chat.id,
                               text='click "save" to save post, or enter other text',
                               reply_markup=keyboards.reply.save())

    if 'save' in message.text.lower():
        with db_session:
            async with state.proxy() as data:
                post_id = data['id']
                text = data['text']
                post = News.get_from_db(news_id=post_id, open_session=db_session)
                if isinstance(post, News):
                    if post.telegram_news_id:
                        await post.edit_message(message_id=post.telegram_news_id,
                                                chat_id=config.config.GROUP_MAIN_ID,
                                                bot=bot,
                                                text=text.replace('*POST TO EDITING*', ''),
                                                edit=False)

                    if post.telegram_news_id_edit:
                        await post.edit_message(message_id=post.telegram_news_id_edit,
                                                chat_id=config.config.GROUP_EDIT_ID,
                                                bot=bot,
                                                text='*POST TO EDITING*\n'+text,
                                                edit=True)

                if state:
                    await state.finish()

                await bot.send_message(chat_id=config.config.GROUP_EDIT_ID,
                                       text='post edited')
