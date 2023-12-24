import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.director_dialogs.transfer_shop_dialog import states

from database.requests.director_requests import DirectorRequests


async def transfer_shop(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал магазин для перемещения - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_transfer_shop=int(item_id), dr_transfer_all_shops=False,
                           dr_sv_whose_shops_will_transfer=None)

    await manager.switch_to(states.TransferShopDirector.select_recipient)


async def transfer_all_by_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Выбрал переместить все магазины по СВ id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_transfer_shop=None, dr_transfer_all_shops=True)

    await manager.switch_to(states.TransferShopDirector.select_shops_by_sv)


async def select_all_shops_for_transfer_by_sv(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал СВ чьи магазины переместить - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_sv_whose_shops_will_transfer=int(item_id))

    await manager.switch_to(states.TransferShopDirector.select_recipient)


async def who_will_take_shop(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал какому СВ переместить магазин - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dr_sv_who_take_shop=int(item_id))

    await manager.switch_to(states.TransferShopDirector.confirm)


async def confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Подтвердил перемещение магазина id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    await DirectorRequests.transfer_shops(
        all_or_not=bool(ctx.dialog_data.get('dr_transfer_all_shops')),
        new_sv_tgid=ctx.dialog_data.get('dr_sv_who_take_shop'),
        old_sv_tgid=ctx.dialog_data.get('dr_sv_whose_shops_will_transfer'),
        shop_tgid=ctx.dialog_data.get('dr_transfer_shop'),
    )

    await c.answer('Выполнено')
    await manager.done()
