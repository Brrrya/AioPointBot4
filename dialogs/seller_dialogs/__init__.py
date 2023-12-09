from aiogram_dialog import Dialog, DialogManager

from dialogs.seller_dialogs.main_message_dialog import windows as main_windows
from dialogs.seller_dialogs.close_shop_dialog import windows as close_shop_window


async def all_shop_dialogs():
    return [
        Dialog(
            await main_windows.plug(),
            await main_windows.main_message(),
            await main_windows.open_photo(),
            await main_windows.open_photo_confirm(),
            await main_windows.rotate_photo(),
            await main_windows.rotate_photo_confirm(),

            on_process_result=main_windows.on_process_result,
        ),
        Dialog(
            await close_shop_window.close_take_rto(),
            await close_shop_window.close_take_ckp(),
            await close_shop_window.close_take_check(),
            await close_shop_window.close_take_dcart(),
            await close_shop_window.close_take_photos(),

        ),
    ]
