import logging

from aiogram_dialog import DialogManager


async def take_date_for_change(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_change_dialog.take_date_for_change>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}

async def change_take_rto(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_change_dialog.change_take_rto>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
    }


async def change_take_ckp(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_change_dialog.change_take_ckp>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
    }


async def change_take_check(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_change_dialog.change_take_check>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
        'ckp_new_data': ctx.dialog_data.get('ckp_new_data')
    }


async def change_take_dcart(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_change_dialog.change_take_dcart>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
        'ckp_new_data': ctx.dialog_data.get('ckp_new_data'),
        'check_new_data': ctx.dialog_data.get('check_new_data')
    }


async def confirm(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Shop.plan_change_dialog.confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
        'ckp_new_data': ctx.dialog_data.get('ckp_new_data'),
        'check_new_data': ctx.dialog_data.get('check_new_data'),
        'dcart_new_data': ctx.dialog_data.get('dcart_new_data'),
    }




