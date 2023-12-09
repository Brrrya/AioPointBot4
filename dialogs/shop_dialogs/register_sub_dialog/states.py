from aiogram.fsm.state import State, StatesGroup


class MainMessageRegistration(StatesGroup):

    badge_scan = State()
    enter_f_name = State()
    enter_l_name = State()
    enter_supervisor = State()
    confirm = State()
    register_code = State()

