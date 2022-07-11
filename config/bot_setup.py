from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import core, models

from config.config import TOKEN


bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

models.create_tables(core.engine)
models.create_tables(core.test_engine)