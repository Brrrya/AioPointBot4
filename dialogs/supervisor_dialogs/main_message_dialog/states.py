from aiogram.fsm.state import State, StatesGroup


class MainMessageSupervisor(StatesGroup):

    main_message = State()

    open_photos = State()
    rotate_photos = State()

    fridge_on_photos = State()
    fridge_off_photos = State()

    close_reports = State()

    checkers = State()

    close_reports_not_today = State()
    close_reports_not_today_show = State()

    structure_changes = State()

