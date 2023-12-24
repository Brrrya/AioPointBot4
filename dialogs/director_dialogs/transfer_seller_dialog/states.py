from aiogram.fsm.state import State, StatesGroup


class TransferSellerDirector(StatesGroup):

    select_seller = State()

    select_recipient = State()
    confirm = State()

    select_sellers_by_sv = State()
