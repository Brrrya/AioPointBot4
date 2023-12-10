from aiogram.fsm.state import State, StatesGroup


class ChangeCheckerSupervisor(StatesGroup):

    select_role = State()
    select_shop = State()
    select_new_checker = State()

    confirm = State()
