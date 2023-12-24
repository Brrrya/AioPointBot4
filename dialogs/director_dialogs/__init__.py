from aiogram_dialog import Dialog, DialogManager

from dialogs.director_dialogs.main_message_dialog import windows as main_message_window
from dialogs.director_dialogs.appoint_supervisor_dialog import windows as appoint_sv_window
from dialogs.director_dialogs.fire_supervisor_dialog import windows as fire_sv_window
from dialogs.director_dialogs.fire_seller_dialog import windows as fire_seller_window
from dialogs.director_dialogs.transfer_seller_dialog import windows as transfer_seller_window


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
        Dialog(
            await fire_seller_window.fire_choice_seller(),
            await fire_seller_window.fire_seller_confirm(),
        ),
        Dialog(
            await transfer_seller_window.select_seller_for_transfer(),
            await transfer_seller_window.who_will_take_sellers(),
            await transfer_seller_window.confirm_seller_transfer(),
            await transfer_seller_window.select_all_seller_for_transfer_by_sv(),
        ),
    ]
