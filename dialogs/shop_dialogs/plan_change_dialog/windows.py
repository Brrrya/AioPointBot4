from datetime import date
import calendar

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format, Const, Case, Multi
from aiogram_dialog.widgets.kbd import Back, Next, Button, Calendar, CalendarConfig, CalendarScope, Row

from aiogram_dialog.widgets.input import MessageInput

from aiogram_dialog.widgets.kbd import Cancel

from dialogs.shop_dialogs.plan_change_dialog import (
    getters, keyboards, selected, states
)


async def take_date_for_change():
    return Window(
        Const('За какую дату изменить план?'),
        keyboards.calendar_for_change_plan(selected.take_date_for_change),
        Cancel(Const('❌ Отмена')),
        getter=getters.take_date_for_change,
        state=states.MainMessageChangePlan.take_date_for_change
    )


async def change_take_rto():
    return Window(
        Format('Данные за {date_for_change}:'),
        Format('Выручка РТО - {rto_old_data}'),
        # Format('Выручка ЦКП - {ckp_old_data}'),
        Format('Количество чеков - {check_old_data}'),
        # Format('Создано дисконт. карт - {dcart_old_data}'),
        Const(' '),
        Const('Новые данные:'),
        Const('Выручка РТО - ❌'),
        # Const('Выручка ЦКП - ❌'),
        Const('Количество чеков - ❌'),
        # Const('Создано дисконт. карт - ❌'),
        Const(' '),
        Const('Введите выручку РТО'),
        Row(
               Cancel(Const('❌ Отмена')),
               Back(Const('⬅️ Назад')),
           ),
        MessageInput(selected.change_take_rto, filter=lambda message: message.text.isdigit()),
        getter=getters.change_take_rto,
        state=states.MainMessageChangePlan.take_rto
    )


# async def change_take_ckp():
#     return Window(
#         Format('Данные за {date_for_change}:'),
#         Format('Выручка РТО - {rto_old_data}'),
#         Format('Выручка ЦКП - {ckp_old_data}'),
#         Format('Количество чеков - {check_old_data}'),
#         Format('Создано дисконт. карт - {dcart_old_data}'),
#         Const(' '),
#         Const('Новые данные:'),
#         Format('Выручка РТО - {rto_new_data}'),
#         Const('Выручка ЦКП - ❌'),
#         Const('Количество чеков - ❌'),
#         Const('Создано дисконт. карт - ❌'),
#         Const(' '),
#         Const('Введите выручку ЦКП'),
#         Row(
#             Cancel(Const('❌ Отмена')),
#             Back(Const('⬅️ Назад')),
#         ),
#         MessageInput(selected.change_take_ckp, filter=lambda message: message.text.isdigit()),
#         getter=getters.change_take_ckp,
#         state=states.MainMessageChangePlan.take_ckp
#     )


async def change_take_check():
    return Window(
        Format('Данные за {date_for_change}:'),
        Format('Выручка РТО - {rto_old_data}'),
        # Format('Выручка ЦКП - {ckp_old_data}'),
        Format('Количество чеков - {check_old_data}'),
        # Format('Создано дисконт. карт - {dcart_old_data}'),
        Const(' '),
        Const('Новые данные:'),
        Format('Выручка РТО - {rto_new_data}'),
        # Format('Выручка ЦКП - {ckp_new_data}'),
        Const('Количество чеков - ❌'),
        # Const('Создано дисконт. карт - ❌'),
        Const(' '),
        Const('Введите количество чеков'),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад')),
        ),
        MessageInput(selected.change_take_check, filter=lambda message: message.text.isdigit()),
        getter=getters.change_take_check,
        state=states.MainMessageChangePlan.take_check
    )


# async def change_take_dcart():
#     return Window(
#         Format('Данные за {date_for_change}:'),
#         Format('Выручка РТО - {rto_old_data}'),
#         Format('Выручка ЦКП - {ckp_old_data}'),
#         Format('Количество чеков - {check_old_data}'),
#         Format('Создано дисконт. карт - {dcart_old_data}'),
#         Const(' '),
#         Const('Новые данные:'),
#         Format('Выручка РТО - {rto_new_data}'),
#         Format('Выручка ЦКП - {ckp_new_data}'),
#         Format('Количество чеков - {check_new_data}'),
#         Const('Создано дисконт. карт - ❌'),
#         Const(' '),
#         Const('Введите количество созданных дисконтных карт'),
#         Row(
#             Cancel(Const('❌ Отмена')),
#             Back(Const('⬅️ Назад')),
#         ),
#         MessageInput(selected.change_take_dcart, filter=lambda message: message.text.isdigit()),
#         getter=getters.change_take_dcart,
#         state=states.MainMessageChangePlan.take_dcart
#     )


async def confirm():
    return Window(
        Format('Данные за {date_for_change}:'),
        Format('Выручка РТО - {rto_old_data}'),
        # Format('Выручка ЦКП - {ckp_old_data}'),
        Format('Количество чеков - {check_old_data}'),
        # Format('Создано дисконт. карт - {dcart_old_data}'),
        Const(' '),
        Const('Новые данные:'),
        Format('Выручка РТО - {rto_new_data}'),
        # Format('Выручка ЦКП - {ckp_new_data}'),
        Format('Количество чеков - {check_new_data}'),
        # Format('Создано дисконт. карт - {dcart_new_data}'),
        Const(' '),
        Const('Все данные для замены верны?'),
        Button(Const('Да'), id='confirm_change_data_in_plan', on_click=selected.confirm),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад')),
        ),
        getter=getters.confirm,
        state=states.MainMessageChangePlan.confirm
    )
