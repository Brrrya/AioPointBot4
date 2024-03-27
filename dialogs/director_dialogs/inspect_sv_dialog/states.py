from aiogram.fsm.state import State, StatesGroup


class InspectSupervisorDirector(StatesGroup):

    main_message = State()
    open_photos = State()
    rotate_photo = State()
    close_reports = State()
    close_reports_not_today = State()
    close_reports_not_today_show = State()
    fridge_on_photos = State()
    fridge_off_photos = State()
