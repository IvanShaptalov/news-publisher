from aiogram.dispatcher.filters.state import StatesGroup, State


class StatesGroup(StatesGroup):
    main_menu = State()
    in_chat = State()
