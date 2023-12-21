from aiogram_dialog import DialogManager

from database.requests.supervisor_requests import SupervisorRequests


async def select_shop_checker(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    role = 'открытия' if ctx.dialog_data.get('checker_role') == 'open' else 'ротации'
    data = await SupervisorRequests.take_all_shops(dialog_manager.event.from_user.id)
    return {
        'checker_role': role,
        'shops': data['shops_list']
    }


async def select_seller_checker(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    role = 'открытия' if ctx.dialog_data.get('checker_role') == 'open' else 'ротации'
    shop = await SupervisorRequests.take_shop_name(ctx.dialog_data.get('shop_tgid_checker'))

    data = await SupervisorRequests.take_all_sellers(dialog_manager.event.from_user.id)
    return {
        'checker_role': role,
        'checker_shop': shop['shop_title'],
        'sellers': data['sellers_list']
    }


async def confirm(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    role = 'открытия' if ctx.dialog_data.get('checker_role') == 'open' else 'ротации'
    shop = await SupervisorRequests.take_shop_name(ctx.dialog_data.get('shop_tgid_checker'))
    if ctx.dialog_data.get('new_checker_tgid'):
        new_checker = await SupervisorRequests.take_data_about_seller_by_tgid(ctx.dialog_data.get('new_checker_tgid'))
    else:
        new_checker = {'full_name': 'убрать'}

    return {
        'checker_role': role,
        'checker_shop': shop['shop_title'],
        'new_checker': new_checker['full_name']
    }
