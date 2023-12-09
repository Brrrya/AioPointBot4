import asyncio

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.supervisor_dialogs.shop_transfer_dialog import states as states_shop_transfer

from database.supervisor_requests import SupervisorRequests


async def shop_choice(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(transfer_shop_tgid=int(item_id), transfer_shop_all=False)
    await manager.switch_to(states_shop_transfer.ShopTransferSupervisor.who_will_take_shop)


async def all_shop_choice(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(transfer_shop_all=True)
    await manager.switch_to(states_shop_transfer.ShopTransferSupervisor.who_will_take_shop)


async def sv_choice(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(transfer_shop_sv_tgid=int(item_id))
    await manager.switch_to(states_shop_transfer.ShopTransferSupervisor.confirm)


async def confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    await SupervisorRequests.shop_transfer(
        current_sv_tgid=c.from_user.id,
        new_sv_tgid=ctx.dialog_data.get('transfer_shop_sv_tgid'),
        shop_tgid=ctx.dialog_data.get('transfer_shop_tgid') if ctx.dialog_data.get('transfer_shop_all') is False else None,
    )
    await manager.done()

