from aiogram.fsm.state import State, StatesGroup


class ShopTransferSupervisor(StatesGroup):

    who_will_transfer_shop = State()
    who_will_take_shop = State()

    confirm = State()

