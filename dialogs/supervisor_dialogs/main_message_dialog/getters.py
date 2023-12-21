from aiogram_dialog import DialogManager

from database.requests.supervisor_requests import SupervisorRequests

async def main_message(dialog_manager: DialogManager, **kwargs):
    result = await SupervisorRequests.get_main_window_info(dialog_manager.event.from_user.id)
    return result


async def open_photos(dialog_manager: DialogManager, **kwargs):
    result = await SupervisorRequests.take_all_open_shops(dialog_manager.event.from_user.id)
    return result


async def rotate_photos(dialog_manager: DialogManager, **kwargs):
    result = await SupervisorRequests.take_all_rotate_shops(dialog_manager.event.from_user.id)
    return result


async def close_reports(dialog_manager: DialogManager, **kwargs):
    result = await SupervisorRequests.close_report_for_dialog(dialog_manager.event.from_user.id)
    return result

async def checkers(dialog_manager: DialogManager, **kwargs):
    result = await SupervisorRequests.take_checkers_data(dialog_manager.event.from_user.id)
    return result