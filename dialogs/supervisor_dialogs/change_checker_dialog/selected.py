import asyncio

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.supervisor_dialogs.change_checker_dialog import states

from database.supervisor_requests import SupervisorRequests


async def change_open(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(checker_role='open')
    await manager.switch_to(states.ChangeCheckerSupervisor.select_shop)


async def change_rotate(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(checker_role='rotate')
    await manager.switch_to(states.ChangeCheckerSupervisor.select_shop)


async def select_shop_checker(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(shop_tgid_checker=int(item_id))
    await manager.switch_to(states.ChangeCheckerSupervisor.select_new_checker)


async def select_seller_checker(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(new_checker_tgid=int(item_id))
    await manager.switch_to(states.ChangeCheckerSupervisor.confirm)


async def remove_seller_checker(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(new_checker_tgid=None)
    await manager.switch_to(states.ChangeCheckerSupervisor.confirm)


async def confirm_new_checker(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()

    await SupervisorRequests.update_checker(
        role=ctx.dialog_data.get('checker_role'),
        shop_tgid=ctx.dialog_data.get('shop_tgid_checker'),
        seller_tgid=ctx.dialog_data.get('new_checker_tgid')
    )

    await c.answer('Готово')
    await manager.done()
