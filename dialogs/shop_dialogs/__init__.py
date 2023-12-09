from aiogram_dialog import Dialog, DialogManager

from dialogs.shop_dialogs.main_message_dialog import windows as main_windows
from dialogs.shop_dialogs.register_sub_dialog import windows as reg_windows
from dialogs.shop_dialogs.plan_update_dialog import windows as new_plan_windows


async def all_shop_dialogs():
    return [
        Dialog(
            await main_windows.main_message(),
            await main_windows.authorization(),
        ),
        Dialog(
            await reg_windows.scan_new_worker_badge(),
            await reg_windows.take_first_name(),
            await reg_windows.take_last_name(),
            await reg_windows.take_supervisor(),
            await reg_windows.confirm_data(),
            await reg_windows.register_code()
        ),
        Dialog(
            await new_plan_windows.update_plan_take_rto(),
            await new_plan_windows.update_plan_take_ckp(),
            await new_plan_windows.update_plan_take_check(),
            await new_plan_windows.update_plan_confirm(),
        ),
    ]
