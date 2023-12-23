from aiogram_dialog import Dialog, DialogManager

from dialogs.director_dialogs.main_message_dialog import windows as main_message_window

async def all_director_dialogs():
    return [
        Dialog(

            await main_message_window.director_main_message(),
        ),
        # Dialog(
        # ),
        # Dialog(
        # ),
        # Dialog(
        # ),
    ]
