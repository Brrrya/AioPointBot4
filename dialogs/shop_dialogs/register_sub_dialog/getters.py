from aiogram_dialog import DialogManager

from database.shop_requests import ShopRequests


async def take_last_name(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'first_name': ctx.dialog_data.get('first_name')
    }


async def take_all_supervisor(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    supervisors = await ShopRequests.take_all_supervisors()
    ctx.dialog_data.update(supervisors=supervisors)
    return {
        'first_name': ctx.dialog_data.get('first_name'),
        'last_name': ctx.dialog_data.get('last_name'),
        'supervisors': supervisors
    }


async def confirm_data(dialog_manager: DialogManager, **kwargs):
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
    ctx = dialog_manager.current_context()
    return {
        'reg_code': ctx.dialog_data.get('reg_code')
            }


