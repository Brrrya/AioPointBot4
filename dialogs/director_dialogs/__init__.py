from aiogram_dialog import Dialog, DialogManager

from dialogs.director_dialogs.main_message_dialog import windows as main_message_window
from dialogs.director_dialogs.appoint_supervisor_dialog import windows as appoint_sv_window
from dialogs.director_dialogs.fire_supervisor_dialog import windows as fire_sv_window


async def all_director_dialogs():
    return [
        Dialog(

            await main_message_window.director_main_message(),
            await main_message_window.structure_changes(),
        ),
        Dialog(
            await appoint_sv_window.choice_new_sv(),
            await appoint_sv_window.confirm(),
        ),
        Dialog(
            await fire_sv_window.fire_choice_sv(),
            await fire_sv_window.fire_confirm(),
        ),
        # Dialog(
        # ),
    ]
