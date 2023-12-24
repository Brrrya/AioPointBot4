import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.director_dialogs.transfer_seller_dialog import states

from database.requests.director_requests import DirectorRequests


async def transfer_seller(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал продавца для перемещения - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_transfer_seller=int(item_id), dr_transfer_all_sellers=False,
                           dr_sv_whose_sellers_will_transfer=None)

    await manager.switch_to(states.TransferSellerDirector.select_recipient)


async def transfer_all_by_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Выбрал переместить всех продавцов по СВ id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_transfer_seller=None, dr_transfer_all_sellers=True)

    await manager.switch_to(states.TransferSellerDirector.select_sellers_by_sv)


async def select_all_seller_for_transfer_by_sv(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал СВ чьих сотрудников переместить - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_sv_whose_sellers_will_transfer=int(item_id))

    await manager.switch_to(states.TransferSellerDirector.select_recipient)


async def who_will_take_sellers(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал какому СВ переместить сотрудника - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_sv_who_take_seller=int(item_id))

    await manager.switch_to(states.TransferSellerDirector.confirm)


async def confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Подтвердил перемещение сотрудника id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    await DirectorRequests.transfer_sellers(
        all_or_not=bool(ctx.dialog_data.get('dr_transfer_all_sellers')),
        new_sv_tgid=ctx.dialog_data.get('dr_sv_who_take_seller'),
        old_sv_tgid=ctx.dialog_data.get('dr_sv_whose_sellers_will_transfer'),
        seller_tgid=ctx.dialog_data.get('dr_transfer_seller'),
    )

    await c.answer('Выполнено')
    await manager.done()
