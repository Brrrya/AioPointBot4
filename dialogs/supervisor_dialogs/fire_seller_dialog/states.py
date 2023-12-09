from aiogram.fsm.state import State, StatesGroup


class SellerFireSupervisor(StatesGroup):

    who_will_fired = State()

    confirm = State()

