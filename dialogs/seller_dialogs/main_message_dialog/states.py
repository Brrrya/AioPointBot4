from aiogram.fsm.state import State, StatesGroup


class MainMessageUser(StatesGroup):

    plug = State()

    main_message = State()

    open_photo = State()
    open_photo_confirm = State()

    rotate_photo = State()
    rotate_photo_confirm = State()

    register_command = State()

    update_plan_choice_day = State()

    fridges_on_photos = State()
    fridges_off_photos = State()
