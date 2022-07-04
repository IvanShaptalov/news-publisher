import os
from abc import abstractmethod
from copy import copy

from aiogram import types

import keyboards.reply.r_snippets
from config import text_util, config
from config.bot_setup import bot
from database import models as db


class BaseSender:

    def __init__(self, event_id, sender_id):
        self.event_id = event_id
        self.sender_id = sender_id
        self.event, self._owner = self._get_event()
        self.sender = self._get_sender()

    def get_answer_markup(self):
        return keyboards.i_snippets.in_chat_inline_keyboard(event_id=self.event_id,
                                                            receiver_chat_id=self.sender_id,
                                                            sender_chat_id=self.get_owner().chat_id,
                                                            current_event_id=self.event_id)

    def check_that_event_exists(self):
        return False if self.event is None else True

    def get_owner(self) -> db.User:
        return self._owner

    def _get_event(self):
        session = db.session
        with session:
            event = db.get_from_db_multiple_filter(table_class=db.Event,
                                                   identifier_to_value=[db.Event.id == self.event_id],
                                                   open_session=session)
            if isinstance(event, db.Event):
                owner = copy(event.event_owner)
                return event, owner
            else:
                return None

    def _get_sender(self) -> db.User:
        sender = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == self.sender_id])
        assert isinstance(sender, db.User)
        return sender

    def prepare_to_send(self):
        text = text_util.NOTIFICATION.format(self.event.title, self.get_owner().user_fullname)
        return text

    @abstractmethod
    def forward_data(self, data):
        pass


class TextSender(BaseSender):
    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        chat_id = self.sender_id

        text = "{} {}".format(self.prepare_to_send(), data.text)

        await bot.send_message(chat_id=chat_id,
                               text=text)


class PhotoSender(BaseSender):
    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        path = os.path.join(config.media_path, 'tmp_photo')
        photo = await data.photo[-1].download(destination_file=path)

        chat_id = self.sender_id

        text = "{}".format(self.prepare_to_send())
        await bot.send_message(chat_id=chat_id,
                               text=text)


class VideoSender(BaseSender):
    async def forward_data(self, data):
        user_in_service_bot = False
        path = os.path.join(config.media_path, 'video.mp4')
        photo = await data.video.download(destination_file=path)

        chat_id = self.sender_id

        text = "{}".format(self.prepare_to_send())

        await bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
        await bot.send_video(chat_id=chat_id,
                                             video=open(path, 'rb'))

