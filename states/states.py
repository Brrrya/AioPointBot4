from aiogram.fsm.state import State, StatesGroup


class UnknownFSM(StatesGroup):
    wait_reg_code = State()
