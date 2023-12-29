from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const

from dialogs.director_dialogs.appoint_supervisor_dialog import (
    getters, keyboards, selected, states
)


async def choice_new_sv():
    return Window(
        Const('Выберете нового управляющего из продавцов'),
        keyboards.choice_new_sv(selected.choice_new_sv),
        Cancel(Const("❌ Отмена")),
        getter=getters.choice_new_sv,
        state=states.AppointSvDirector.choice_new_sv
    )


async def confirm():
    return Window(
        Format('Повысить сотрудника {seller_name} до управляющего?'),
        Const(' '),
        Const('Потом сотрудника можно будет только уволить и ему надо будет заново регистрироваться в боте'),
        Button(Const('⬆️ Повысить'), on_click=selected.confirm, id='dr_confirm_appoint_sv'),
        Row(
            Cancel(Const("❌ Отмена")),
            Back(Const("⬅️ Назад")),
        ),
        getter=getters.confirm,
        state=states.AppointSvDirector.confirm
    )
