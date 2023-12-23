from aiogram.fsm.state import State, StatesGroup


class AppointSvDirector(StatesGroup):

    choice_new_sv = State()
    confirm = State()

