from aiogram.fsm.state import State, StatesGroup


class MainMessageUserClose(StatesGroup):

    close_take_rto = State()
    close_take_ckp = State()
    close_take_check = State()
    close_take_dcart = State()

    close_take_photos = State()

    close_take_enter_photo = State()


