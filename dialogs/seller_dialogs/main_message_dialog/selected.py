from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.seller_dialogs.main_message_dialog import states as states_main_message
from dialogs.seller_dialogs.close_shop_dialog import states as states_close_dialog

from database.seller_requests import SellerRequests


async def to_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def open_button(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(states_main_message.MainMessageUser.open_photo)


async def open_photo(m: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(open_photo=m.photo[-1].file_id)
    await manager.switch_to(states_main_message.MainMessageUser.open_photo_confirm)


async def open_photo_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    await SellerRequests.insert_photo(c.from_user.id, 'open', [ctx.dialog_data.get('open_photo')])
    shop = await SellerRequests.take_main_window_info(c.from_user.id)
    await manager.bg(shop['shop_tgid'], shop['shop_tgid']).update(data=manager.start_data)
    await c.message.answer('Сохранено!')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def rotate_button(m: Message, widget: MessageInput, manager: DialogManager):
    await manager.switch_to(states_main_message.MainMessageUser.rotate_photo)


async def rotate_photo(m: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(rotate_photo=m.photo[-1].file_id)
    await manager.switch_to(states_main_message.MainMessageUser.rotate_photo_confirm)


async def rotate_photo_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    await SellerRequests.insert_photo(c.from_user.id, 'rotate', [ctx.dialog_data.get('rotate_photo')])
    shop = await SellerRequests.take_main_window_info(c.from_user.id)
    await manager.bg(shop['shop_tgid'], shop['shop_tgid']).update(data=manager.start_data)
    await c.message.answer('Сохранено!')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def close_button(m: Message, widget: MessageInput, manager: DialogManager):
    await manager.start(states_close_dialog.MainMessageUserClose.close_take_rto)


async def change_plan_button(m: Message, widget: MessageInput, manager: DialogManager):
    print('change plan button')

