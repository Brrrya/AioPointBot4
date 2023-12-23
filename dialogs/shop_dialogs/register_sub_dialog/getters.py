import logging

from aiogram_dialog import DialogManager

from database.requests.shop_requests import ShopRequests

async def scan_new_worker_badge(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.register.scan_new_worker_badge>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}


async def take_first_name(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.register.take_first_name>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}


async def take_last_name(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.register.take_last_name>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'first_name': ctx.dialog_data.get('first_name')
    }


async def take_all_supervisor(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.register.take_supervisor>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    supervisors = await ShopRequests.take_all_supervisors()
    ctx.dialog_data.update(supervisors=supervisors)
    return {
        'first_name': ctx.dialog_data.get('first_name'),
        'last_name': ctx.dialog_data.get('last_name'),
        'supervisors': supervisors
    }


async def confirm_data(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.register.confirm_data>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    supervisors = ctx.dialog_data.get('supervisors')
    for i in supervisors:
        if int(i[1]) == int(ctx.dialog_data.get('supervisor')):
            res = i[0]
    return {
        'first_name': ctx.dialog_data.get('first_name'),
        'last_name': ctx.dialog_data.get('last_name'),
        'supervisor': res
    }


async def register_code(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.register.register_code>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()
    return {
        'reg_code': ctx.dialog_data.get('reg_code')
            }


