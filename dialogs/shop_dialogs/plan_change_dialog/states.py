from aiogram.fsm.state import State, StatesGroup


class MainMessageChangePlan(StatesGroup):

    take_date_for_change = State()

    take_rto = State()
    # take_ckp = State()
    take_check = State()
    # take_dcart = State()

    confirm = State()

