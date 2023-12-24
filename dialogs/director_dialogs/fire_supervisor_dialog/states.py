from aiogram.fsm.state import State, StatesGroup


class FireSvDirector(StatesGroup):

    fire_choice_sv = State()
    fire_confirm = State()

