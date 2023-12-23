import logging

from aiogram_dialog import DialogManager

from database.requests.supervisor_requests import SupervisorRequests


async def who_will_transfer_shop(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.shop_transfer_dialog.who_will_transfer_shop>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    return await SupervisorRequests.take_all_shops(dialog_manager.event.from_user.id)


async def who_will_take_shop(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.shop_transfer_dialog.who_will_take_shop>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    return await SupervisorRequests.take_all_sv()


async def confirm(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Supervisor.shop_transfer_dialog.confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()
    data = await SupervisorRequests.take_data_for_shop_transfer(
        sv_tgid=ctx.dialog_data.get('transfer_shop_sv_tgid'),
        shop_tgid=ctx.dialog_data.get('transfer_shop_tgid') if ctx.dialog_data.get('transfer_shop_all') is False else None,
    )

    return {
        'transfer_shop_title': 'все магазины' if ctx.dialog_data.get('transfer_shop_all') is True else data['shop_title'],
        'transfer_shop_sv_name': data['sv_name']
    }
