from aiogram import F

from aiogram_dialog import Window, DialogManager, Data

from aiogram_dialog.widgets.text import Format, Const, List, Multi, Case
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media.static import ContentType
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia


from dialogs.supervisor_dialogs.fire_seller_dialog import (
    getters, keyboards, selected, states
)


async def who_will_deleted():
    return Window(
        Case(
            {
                True:
                    Const("Какого сотрудника удалить из базы данных?"),
                False:
                    Const('За вами никто не закреплен')
            },
            selector='more_then_nobody'
        ),
        keyboards.all_sellers_by_sv(
            seller_choice=selected.seller_choice,
        ),
        Cancel(Const('Отмена')),
        getter=getters.who_will_deleted,
        state=states.SellerFireSupervisor.who_will_fired
    )


async def confirm():
    return Window(
        Format('Вы уверены что хотите удалить сотрудника - {full_name}?'),
        Const(' '),
        Const('Вернуться он сможет только заново зарегистрировавшись'),
        Button(Const("Да"), id='confirm_fire_seller', on_click=selected.confirm),
        Row(
            Cancel(Const('Отмена')),
            Back(Const('Назад'))
        ),
        getter=getters.confirm,
        state=states.SellerFireSupervisor.confirm
    )
