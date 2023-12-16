import asyncio
import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.supervisor_dialogs.seller_transfer_dialog import states as states_seller_transfer

from database.supervisor_requests import SupervisorRequests


async def seller_choice(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'СВ | Выбрал сотрудника для передачи другому СВ - {item_id}id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(transfer_seller_tgid=int(item_id), transfer_seller_all=False)
    await manager.switch_to(states_seller_transfer.SellerTransferSupervisor.who_will_take_seller)


async def all_seller_choice(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Выбрал всех сотрудников для передачи другому СВ id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(transfer_seller_all=True)
    await manager.switch_to(states_seller_transfer.SellerTransferSupervisor.who_will_take_seller)


async def sv_choice(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'СВ | Выбрал нового СВ для перемещаемых сотрудников - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(transfer_seller_sv_tgid=int(item_id))
    await manager.switch_to(states_seller_transfer.SellerTransferSupervisor.confirm)


async def confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Подтвердил передачу сотрудников другому СВ id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    await SupervisorRequests.seller_transfer(
        current_sv_tgid=c.from_user.id,
        new_sv_tgid=ctx.dialog_data.get('transfer_seller_sv_tgid'),
        seller_tgid=ctx.dialog_data.get('transfer_seller_tgid') if ctx.dialog_data.get('transfer_seller_all') is False else None,
    )
    await manager.done()

