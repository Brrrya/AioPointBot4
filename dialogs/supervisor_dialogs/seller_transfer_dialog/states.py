from aiogram.fsm.state import State, StatesGroup


class SellerTransferSupervisor(StatesGroup):

    who_will_transfer = State()
    who_will_take_seller = State()

    confirm = State()

