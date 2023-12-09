from aiogram.fsm.state import State, StatesGroup


class MainMessageSupervisor(StatesGroup):

    main_message = State()

    open_photos = State()
    rotate_photos = State()

    checkers = State()

    # transfer_seller = State()
    # transfer_shop = State()

    structure_changes = State()

