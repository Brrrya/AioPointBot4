import logging

from aiogram_dialog import DialogManager


async def take_rto(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Shop.plan_update.update_plan_take_rto>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}

async def take_ckp(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_update.update_plan_take_ckp>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'rto': ctx.dialog_data.get('rto')
    }


async def take_check(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_update.update_plan_take_check>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'rto': ctx.dialog_data.get('rto'),
        'ckp': ctx.dialog_data.get('ckp'),
    }


async def confirm(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_update.update_plan_confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'rto': ctx.dialog_data.get('rto'),
        'ckp': ctx.dialog_data.get('ckp'),
        'check': ctx.dialog_data.get('check'),
    }

