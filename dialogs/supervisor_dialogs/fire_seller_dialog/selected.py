import asyncio

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.supervisor_dialogs.fire_seller_dialog import states
from dialogs.seller_dialogs.main_message_dialog import states as states_seller

from database.supervisor_requests import SupervisorRequests


async def seller_choice(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(fire_seller_tgid=int(item_id))
    await manager.switch_to(states.SellerFireSupervisor.confirm)


async def confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    seller_tgid = ctx.dialog_data.get('fire_seller_tgid')
    res = await SupervisorRequests.delete_seller(
        seller_tgid=seller_tgid
    )

    if res['update_message'] is True:
        await manager.bg(res['shop_with_seller_tgid'], res['shop_with_seller_tgid']).update(data=manager.start_data)
        await manager.bg(seller_tgid, seller_tgid).switch_to(states_seller.MainMessageUser.plug)

    await manager.done()

