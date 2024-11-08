import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.shop_dialogs.plan_update_dialog import states
from dialogs.shop_dialogs.main_message_dialog import states as main_dialog_states

from database.requests.plan_requests import PlanRequests


async def take_rto(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Магазин | Ввел план по РТО - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(rto=m.text)
    await manager.switch_to(states.MainMessageUpdatePlan.take_check)


# async def take_ckp(m: Message, widget: MessageInput, manager: DialogManager):
#     logging.info(f'Магазин | Ввел план по ЦКП - {m.text} id={m.from_user.id} username={m.from_user.username}')
#
#     ctx = manager.current_context()
#     ctx.dialog_data.update(ckp=m.text)
#     await manager.switch_to(states.MainMessageUpdatePlan.take_check)


async def take_check(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Магазин | Ввел план по чекам - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(check=m.text)
    await manager.switch_to(states.MainMessageUpdatePlan.confirm)


async def confirm(call: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Магазин | Подтвердил ввод плана id={call.from_user.id} username={call.from_user.username}')

    ctx = manager.current_context()

    await PlanRequests.update_plan(
        rto=int(ctx.dialog_data.get('rto')),
        check=int(ctx.dialog_data.get('check')),
        shop_tgid=int(call.from_user.id),
    )

    await call.message.answer('План обновлен!')
    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=main_dialog_states.MainMessage.main_message)
