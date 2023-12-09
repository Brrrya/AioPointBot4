from aiogram.fsm.state import State, StatesGroup


class MainMessageUpdatePlan(StatesGroup):

    take_rto = State()
    take_ckp = State()
    take_check = State()
    confirm = State()

