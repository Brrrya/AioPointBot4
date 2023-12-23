import logging

from aiogram_dialog import DialogManager

from database.requests.supervisor_requests import SupervisorRequests


async def who_will_deleted(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.fire_seller.who_will_deleted>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    return await SupervisorRequests.take_all_sellers(dialog_manager.event.from_user.id)


async def confirm(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.fire_seller.confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()
    data = await SupervisorRequests.take_data_about_seller_by_tgid(ctx.dialog_data.get('fire_seller_tgid'))
    return data
