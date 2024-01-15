from aiogram_dialog import Dialog

from dialogs.supervisor_dialogs.main_message_dialog import windows as main_windows
from dialogs.supervisor_dialogs.change_checker_dialog import windows as change_checker_window
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
            await main_windows.checkers(),
            await main_windows.close_reports(),
            await main_windows.close_reports_not_today(),
            await main_windows.close_reports_not_today_show(),

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
        Dialog(
            await change_checker_window.select_role_checker(),
            await change_checker_window.select_shop_checker(),
            await change_checker_window.select_seller_checker(),
            await change_checker_window.confirm(),
        ),
    ]
