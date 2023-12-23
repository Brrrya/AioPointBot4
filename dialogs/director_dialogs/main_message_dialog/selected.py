import logging

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.supervisor_dialogs.fire_seller_dialog import states
from dialogs.seller_dialogs.main_message_dialog import states as states_seller

from database.requests.supervisor_requests import SupervisorRequests


async def seller_choice(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):

    ctx = manager.current_context()
    ctx.dialog_data.update(fire_seller_tgid=int(item_id))
    await manager.switch_to(states.SellerFireSupervisor.confirm)

