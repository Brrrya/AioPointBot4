import logging

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests
from database.requests.supervisor_requests import SupervisorRequests


async def main_message(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.inspect_sv.main_message>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    result = await SupervisorRequests.get_main_window_info(ctx.start_data.get('dr_inspected_sv'))
    return result


async def open_photos(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.inspect_sv.open_photos>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    result = await SupervisorRequests.take_all_open_shops(ctx.start_data.get('dr_inspected_sv'))
    return result


async def rotate_photos(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.inspect_sv.rotate_photos>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    result = await SupervisorRequests.take_all_rotate_shops(ctx.start_data.get('dr_inspected_sv'))
    return result


async def close_reports(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.inspect_sv.close_reports>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    res = {
        'all_not_close_report': (
            (shop_name,) for shop_name in ctx.dialog_data.get('who_not_send_report')  # Список ещё не отправивших отчёт закрытия
        ),
        'close_report_or_not': False if ctx.dialog_data.get('who_not_send_report') else True  # Если все отправили отчёт закрытия то True
    }
    return res
