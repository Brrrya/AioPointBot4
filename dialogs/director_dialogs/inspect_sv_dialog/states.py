from aiogram.fsm.state import State, StatesGroup


class InspectSupervisorDirector(StatesGroup):

    main_message = State()
    open_photos = State()
    rotate_photo = State()
    close_reports = State()
