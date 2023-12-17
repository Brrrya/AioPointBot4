import logging
from datetime import date

from aiogram.types import CallbackQuery, Message, FSInputFile

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import MessageInput

from dialogs.shop_dialogs.plan_change_dialog import states
from dialogs.shop_dialogs.main_message_dialog import states as main_dialog_states


from database.plan_requests import PlanRequests


async def take_date_for_change(m: Message, widget, manager: DialogManager, select_date: date):
    logging.info(f'Магазин | Выбрал дату изменения плана - {select_date} id={m.from_user.id} username={m.from_user.username}')

    data = await PlanRequests.data_for_that_day(
        select_date,
        m.from_user.id
    )

    ctx = manager.current_context()
    ctx.dialog_data.update(
        date_for_change=str(select_date),
        rto_old_data=data['rto_old_data'],
        ckp_old_data=data['ckp_old_data'],
        check_old_data=data['check_old_data'],
        dcart_old_data=data['dcart_old_data'],
    )
    await manager.switch_to(states.MainMessageChangePlan.take_rto)


async def change_take_rto(m: Message, widget, manager: DialogManager):
    logging.info(f'Магазин | Ввел новый данные РТО - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(rto_new_data=m.text)
    await manager.switch_to(states.MainMessageChangePlan.take_ckp)


async def change_take_ckp(m: Message, widget, manager: DialogManager):
    logging.info(f'Магазин | Ввел новый данные ЦКП - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(ckp_new_data=m.text)
    await manager.switch_to(states.MainMessageChangePlan.take_check)


async def change_take_check(m: Message, widget, manager: DialogManager):
    logging.info(f'Магазин | Ввел новый данные чеков - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(check_new_data=m.text)
    await manager.switch_to(states.MainMessageChangePlan.take_dcart)


async def change_take_dcart(m: Message, widget, manager: DialogManager):
    logging.info(f'Магазин | Ввел новый данные дисконтных карт - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(dcart_new_data=m.text)
    await manager.switch_to(states.MainMessageChangePlan.confirm)


async def confirm(c: CallbackQuery, widget, manager: DialogManager):
    logging.info(f'Магазин | Подтвердил замену старых данных на новые id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    await PlanRequests.change_data_in_plan(
        date_for_change=str(ctx.dialog_data.get('date_for_change')),
        rto_new_data=int(ctx.dialog_data.get('rto_new_data')),
        ckp_new_data=int(ctx.dialog_data.get('ckp_new_data')),
        check_new_data=int(ctx.dialog_data.get('check_new_data')),
        dcart_new_data=int(ctx.dialog_data.get('dcart_new_data')),
        shop_tgid=c.from_user.id
    )
    await c.message.answer(f'Данные за {ctx.dialog_data.get("date_for_change")} обновлены!')
    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=main_dialog_states.MainMessage.main_message)


