import logging

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests


async def select_shops_for_transfer(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_shops.select_shops_for_transfer>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_shops()

    return {
        'shops': data
    }


async def select_all_shops_for_transfer_by_sv(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_shops.select_all_shops_for_transfer_by_sv>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_supervisors()

    return {
        'supervisors': data
    }

async def who_will_take_shops(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_shops.who_will_take_shops>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_supervisors()

    return {
        'supervisors': data
    }



async def confirm_shop_transfer(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_shops.confirm_shop_transfer>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    data = await DirectorRequests.take_data_for_transfer_shop(
        old_sv_tgid=ctx.dialog_data.get('dr_sv_whose_shops_will_transfer'),
        new_sv_tgid=int(ctx.dialog_data.get('dr_sv_who_take_shop')),
        shop_tgid=ctx.dialog_data.get('dr_transfer_shop'),
        all_or_not=bool(ctx.dialog_data.get('dr_transfer_shop')),
    )

    return {
        'all_or_not': ctx.dialog_data.get('dr_transfer_all_shops'),
        'shop_name': data['shop_data']['full_name'],
        'old_sv_name': data['old_sv_data']['full_name'],
        'new_sv_name': data['new_sv_data']['full_name'],
    }

