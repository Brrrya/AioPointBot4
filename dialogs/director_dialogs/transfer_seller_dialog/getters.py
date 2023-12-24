import logging

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests


async def select_seller_for_transfer(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_seller.select_seller_for_transfer>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_workers()

    return {
        'sellers': data
    }


async def select_all_seller_for_transfer_by_sv(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_seller.select_all_seller_for_transfer_by_sv>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_supervisors()

    return {
        'supervisors': data
    }

async def who_will_take_sellers(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_seller.who_will_take_sellers>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_supervisors()

    return {
        'supervisors': data
    }



async def confirm_seller_transfer(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.transfer_seller.confirm_seller_transfer>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    data = await DirectorRequests.take_data_for_transfer_seller(
        old_sv_tgid=ctx.dialog_data.get('dr_sv_whose_sellers_will_transfer'),
        new_sv_tgid=int(ctx.dialog_data.get('dr_sv_who_take_seller')),
        seller_tgid=ctx.dialog_data.get('dr_transfer_seller'),
        all_or_not=bool(ctx.dialog_data.get('dr_transfer_seller')),
    )

    return {
        'all_or_not': ctx.dialog_data.get('dr_transfer_all_sellers'),
        'seller_name': data['seller_data']['full_name'],
        'old_sv_name': data['old_sv_data']['full_name'],
        'new_sv_name': data['new_sv_data']['full_name'],
    }

