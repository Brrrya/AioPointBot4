from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format, Const, Case, Multi
from aiogram_dialog.widgets.kbd import Back, Next, Button
from aiogram_dialog.widgets.input import MessageInput

from aiogram_dialog.widgets.kbd import Cancel

from dialogs.shop_dialogs.plan_update_dialog import (
    getters, keyboards, selected, states
)


async def update_plan_take_rto():
    return Window(
        Format('РТО - '),
        Format('Чеки - '),
        Const(' '),
        Const('Введите план РТО на месяц'),
        MessageInput(selected.take_rto, filter=lambda message: message.text.isdigit()),
        Cancel(Const('❌ Отмена')),
        getter=getters.take_rto,
        state=states.MainMessageUpdatePlan.take_rto
    )


# async def update_plan_take_ckp():
#     return Window(
#         Format('РТО - {rto}'),
#         Format('ЦКП - '),
#         Format('Чеки - '),
#         Const(' '),
#         Const('Введите план ЦКП на месяц'),
#         Back(Const("⬅️ Назад")),
#         Cancel(Const('❌ Отмена')),
#         MessageInput(selected.take_ckp, filter=lambda message: message.text.isdigit()),
#         getter=getters.take_ckp,
#         state=states.MainMessageUpdatePlan.take_ckp
#     )


async def update_plan_take_check():
    return Window(
        Format('РТО - {rto}'),
        Format('Чеки - '),
        Const(' '),
        Const('Введите план чеков на месяц'),
        Back(Const("⬅️ Назад")),
        Cancel(Const('️❌ Отмена')),
        MessageInput(selected.take_check, filter=lambda message: message.text.isdigit()),
        getter=getters.take_check,
        state=states.MainMessageUpdatePlan.take_check
    )


async def update_plan_confirm():
    return Window(
        Format('РТО - {rto}'),
        Format('Чеки - {check}'),
        Const(' '),
        Const('Данные верны?'),
        Button(Const('✅ Да'), on_click=selected.confirm, id='confirm_update_plan'),
        Back(Const("⬅️ Назад")),
        Cancel(Const('❌ Отмена')),
        getter=getters.confirm,
        state=states.MainMessageUpdatePlan.confirm
    )

