from aiogram_dialog import Dialog

from dialogs.supervisor_dialogs.main_message_dialog import windows as main_windows
# from dialogs.supervisor_dialogs.change_open_checker_dialog import windows as change_open_windows
# from dialogs.supervisor_dialogs.change_rotate_checker_dialog import windows as change_rotate_windows
from dialogs.supervisor_dialogs.seller_transfer_dialog import windows as seller_transfer_windows
from dialogs.supervisor_dialogs.shop_transfer_dialog import windows as shop_transfer_windows
from dialogs.supervisor_dialogs.fire_seller_dialog import windows as fire_seller_windows


async def all_supervisor_dialogs():
    return [
        Dialog( # мейн виндов
            await main_windows.main_message(),
            await main_windows.open_photos(),
            await main_windows.rotate_photos(),
            await main_windows.structure_changes(),

            on_process_result=main_windows.on_process_result,
        ),
        Dialog(
            await seller_transfer_windows.who_will_transfer(),
            await seller_transfer_windows.who_will_take_seller(),
            await seller_transfer_windows.confirm(),
        ),
        Dialog(
            await shop_transfer_windows.who_will_transfer_shop(),
            await shop_transfer_windows.who_will_take_shop(),
            await shop_transfer_windows.confirm(),
        ),
        Dialog(
            await fire_seller_windows.who_will_deleted(),
            await fire_seller_windows.confirm(),
        ),
    ]
