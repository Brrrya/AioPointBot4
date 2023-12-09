import random

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import MessageInput

from dialogs.shop_dialogs.register_sub_dialog import states
from dialogs.shop_dialogs.main_message_dialog import states as main_dialog_states


from database.shop_requests import ShopRequests


async def take_register_badge(m: Message, widget: MessageInput, manager: DialogManager):
    data = await ShopRequests.badge_check(int(m.text))
    if data is False:
        await manager.event.answer("Данный бейджик уже зарегистрирован!")
    else:
        ctx = manager.current_context()
        ctx.dialog_data.update(badge=m.text)
        await manager.switch_to(states.MainMessageRegistration.enter_f_name)


async def take_first_name(m: Message, widget: MessageInput, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    ctx.dialog_data.update(first_name=m.text)
    await dialog_manager.switch_to(states.MainMessageRegistration.enter_l_name)


async def take_last_name(m: Message, widget: MessageInput, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    ctx.dialog_data.update(last_name=m.text)
    await dialog_manager.switch_to(states.MainMessageRegistration.enter_supervisor)


async def take_supervisor(call: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    ctx = dialog_manager.current_context()
    ctx.dialog_data.update(supervisor=int(item_id))
    await dialog_manager.switch_to(states.MainMessageRegistration.confirm)


async def confirm_data(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    ctx = dialog_manager.current_context()
    reg_code = random.randint(100000, 999999)
    ctx.dialog_data.update(reg_code=reg_code)
    await ShopRequests.insert_new_reg_user_in_db(
        first_name=ctx.dialog_data.get('first_name'),
        last_name=ctx.dialog_data.get('last_name'),
        supervisor_tgid=int(ctx.dialog_data.get('supervisor')),
        badge=int(ctx.dialog_data.get('badge')),
        reg_code=int(reg_code)
    )
    await dialog_manager.switch_to(states.MainMessageRegistration.register_code)


async def coplete_register(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.reset_stack()
    await dialog_manager.start(mode=StartMode.RESET_STACK, state=main_dialog_states.MainMessage.main_message)




