import asyncio

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.supervisor_dialogs.main_message_dialog import states as states_main_message
from dialogs.supervisor_dialogs.seller_transfer_dialog import states as states_transfer_seller
from dialogs.supervisor_dialogs.shop_transfer_dialog import states as states_transfer_shop
from dialogs.supervisor_dialogs.fire_seller_dialog import states as states_fire_seller


from database.supervisor_requests import SupervisorRequests


async def refresh_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.bg(c.from_user.id, c.from_user.id).update(data=manager.start_data)


async def back_to_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(states_main_message.MainMessageSupervisor.main_message)


async def open_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    all_photos = await SupervisorRequests.take_all_photo_rotate_or_state(int(c.from_user.id), 'open')
    for photo in all_photos:
        await c.message.answer_photo(photo=photo[0], caption=photo[1])
    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=states_main_message.MainMessageSupervisor.open_photos)


async def rotate_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    all_photos = await SupervisorRequests.take_all_photo_rotate_or_state(int(c.from_user.id), 'rotate')
    for photo in all_photos:
        await c.message.answer_photo(photo=photo[0], caption=photo[1])
    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=states_main_message.MainMessageSupervisor.rotate_photos)


async def change_structure(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(states_main_message.MainMessageSupervisor.structure_changes)


async def checkers(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(states_main_message.MainMessageSupervisor.checkers)


async def transfer_seller(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(states_transfer_seller.SellerTransferSupervisor.who_will_transfer)


async def transfer_shop(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(states_transfer_shop.ShopTransferSupervisor.who_will_transfer_shop)


async def fire_seller(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(states_fire_seller.SellerFireSupervisor.who_will_fired)

