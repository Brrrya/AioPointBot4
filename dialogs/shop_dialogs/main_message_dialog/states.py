from aiogram.fsm.state import State, StatesGroup


class MainMessage(StatesGroup):

    main_message = State()
    auth_wait_badge = State()


