from aiogram import F

from aiogram_dialog import Window, DialogManager, Data

from aiogram_dialog.widgets.text import Format, Const, List, Multi, Case
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media.static import ContentType
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia


from dialogs.director_dialogs.fire_seller_dialog import (
    getters, keyboards, selected, states
)


async def fire_choice_seller():
    return Window(
        Const("Выберете продавца для увольнения"),
        keyboards.choice_seller(
            on_click=selected.fire_choice_seller
        ),
        Cancel(Const('Отмена')),
        getter=getters.fire_choice_seller,
        state=states.FireSellerDirector.fire_choice_seller
    )


async def fire_seller_confirm():
    return Window(
        Format('Вы действительно хотите уволить сотрудника {full_name}'),
        Button(Const('Уволить'), id='dr_confirm_fire_seller', on_click=selected.fire_seller_confirm),
        Row(
            Cancel(Const('Отмена')),
            Back(Const('Назад'))
        ),
        getter=getters.fire_seller_confirm,
        state=states.FireSellerDirector.fire_confirm
    )

