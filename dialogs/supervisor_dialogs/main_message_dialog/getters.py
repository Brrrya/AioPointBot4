import logging

from aiogram_dialog import DialogManager

from database.requests.supervisor_requests import SupervisorRequests


async def main_message(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.main_message>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    result = await SupervisorRequests.get_main_window_info(dialog_manager.event.from_user.id)
    return result


async def open_photos(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.open_photo>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    result = await SupervisorRequests.take_all_open_shops(dialog_manager.event.from_user.id)
    return result


async def rotate_photos(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.rotate_photos>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    result = await SupervisorRequests.take_all_rotate_shops(dialog_manager.event.from_user.id)
    return result


async def fridges_on_photos(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.fridges_on_photos>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    res = {
        'all_not_fridge_on': (
            (shop_name,) for shop_name in ctx.dialog_data.get('who_not_fridge_on')  # Список ещё не отправивших фото вкл ХО
        ),
        'fridge_on_or_off': False if ctx.dialog_data.get('who_not_fridge_on') else True  # Если все отправили фото вкл ХО то True
    }

    return res


async def fridges_off_photos(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.fridges_off_photos>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    res = {
        'all_not_fridge_off': (
            (shop_name,) for shop_name in ctx.dialog_data.get('who_not_fridge_off')  # Список ещё не отправивших фото вкл ХО
        ),
        'fridge_off_or_on': False if ctx.dialog_data.get('who_not_fridge_off') else True  # Если все отправили фото вкл ХО то True
    }

    return res


async def close_reports(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.close_reports>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    res = {
        'all_not_close_report': (
            (shop_name,) for shop_name in ctx.dialog_data.get('who_not_send_report')  # Список ещё не отправивших отчёт закрытия
        ),
        'close_report_or_not': False if ctx.dialog_data.get('who_not_send_report') else True  # Если все отправили отчёт закрытия то True
    }

    return res


async def structure_changes(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.structure_changes>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    return {}


async def checkers(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.checkers>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    result = await SupervisorRequests.take_checkers_data(dialog_manager.event.from_user.id)
    return result


async def close_reports_not_today(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.main_dialog.close_reports_not_today>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    return {}

