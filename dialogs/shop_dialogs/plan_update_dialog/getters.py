from aiogram_dialog import DialogManager

from database.shop_requests import ShopRequests


async def take_ckp(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'rto': ctx.dialog_data.get('rto')
    }


async def take_check(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'rto': ctx.dialog_data.get('rto'),
        'ckp': ctx.dialog_data.get('ckp'),
    }


async def confirm(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'rto': ctx.dialog_data.get('rto'),
        'ckp': ctx.dialog_data.get('ckp'),
        'check': ctx.dialog_data.get('check'),
    }

