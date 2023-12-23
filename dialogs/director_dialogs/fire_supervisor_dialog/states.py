from aiogram.fsm.state import State, StatesGroup


class MainMessageDirector(StatesGroup):

    select_sv = State()
    confirm = State()

