from aiogram.fsm.state import State, StatesGroup


class FireSellerDirector(StatesGroup):

    fire_choice_seller = State()
    fire_confirm = State()

