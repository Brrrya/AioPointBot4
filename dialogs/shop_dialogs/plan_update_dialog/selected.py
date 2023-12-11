from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import MessageInput

from dialogs.shop_dialogs.plan_update_dialog import states
from dialogs.shop_dialogs.main_message_dialog import states as main_dialog_states


from database.shop_requests import ShopRequests
from database.plan_requests import PlanRequests


async def take_rto(m: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(rto=m.text)
    await manager.switch_to(states.MainMessageUpdatePlan.take_ckp)


async def take_ckp(m: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(ckp=m.text)
    await manager.switch_to(states.MainMessageUpdatePlan.take_check)


async def take_check(m: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(check=m.text)
    await manager.switch_to(states.MainMessageUpdatePlan.confirm)


async def confirm(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()

    await PlanRequests.update_plan(
        rto=int(ctx.dialog_data.get('rto')),
        ckp=int(ctx.dialog_data.get('ckp')),
        check=int(ctx.dialog_data.get('check')),
        shop_tgid=int(call.from_user.id),
    )

    await call.message.answer('План обновлен!')
    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=main_dialog_states.MainMessage.main_message)
