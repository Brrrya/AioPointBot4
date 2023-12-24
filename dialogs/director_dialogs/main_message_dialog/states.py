from aiogram.fsm.state import State, StatesGroup


class MainMessageDirector(StatesGroup):

    main_message = State()
    structure_changes = State()
    inspect_sv = State()
