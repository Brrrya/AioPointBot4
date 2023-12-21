from aiogram_dialog import DialogManager

from database.requests.supervisor_requests import SupervisorRequests


async def who_will_transfer(dialog_manager: DialogManager, **kwargs):
    return await SupervisorRequests.take_all_sellers(dialog_manager.event.from_user.id)


async def who_will_take_seller(**kwargs):
    return await SupervisorRequests.take_all_sv()


async def confirm(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    data = await SupervisorRequests.take_data_for_seller_transfer(
        sv_tgid=ctx.dialog_data.get('transfer_seller_sv_tgid'),
        seller_tgid=ctx.dialog_data.get('transfer_seller_tgid') if ctx.dialog_data.get('transfer_seller_all') is False else None,
    )

    return {
        'transfer_seller_name': 'всех сотрудников' if ctx.dialog_data.get('transfer_seller_all') is True else data['seller_name'],
        'transfer_seller_sv_name': data['sv_name']
    }
