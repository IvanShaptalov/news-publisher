from aiogram import types
from config import text_util


def inline_button(text, data) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text, callback_data=data)


def editing_post_inline_keyboard(post_id: int) -> types.InlineKeyboardMarkup:
    """
    send inline keyboard if user not in chat
    :param post_id: post id
    :return: types.InlineKeyboardMarkup
    """

    return types.InlineKeyboardMarkup(). \
        add(
        inline_button(text_util.EDIT_POST, f'{text_util.EDIT_POST}:{post_id}'),
        inline_button(text_util.DELETE_POST, f'{text_util.DELETE_POST}:{post_id}')
    )
