from aiogram.fsm.state import State, StatesGroup


class TransferShopDirector(StatesGroup):

    select_shop = State()

    select_recipient = State()
    confirm = State()

    select_shops_by_sv = State()
