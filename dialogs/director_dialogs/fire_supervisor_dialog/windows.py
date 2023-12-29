from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const, Multi, Case

from dialogs.director_dialogs.fire_supervisor_dialog import (
    getters, keyboards, selected, states
)


async def fire_choice_sv():
    return Window(
        Const("Выберете супервайзера для увольнения"),
        Const(" "),
        Const("Чтобы уволить супервайзера, необходимо, чтобы за ним не было закреплено магазинов и сотрудников!"),
        keyboards.choice_sv(
            on_click=selected.fire_choice_sv
        ),
        Cancel(Const('❌ Отмена')),
        getter=getters.fire_choice_sv,
        state=states.FireSvDirector.fire_choice_sv
    )


async def fire_confirm():
    return Window(
        Case(
            {
                True: Format('Вы действительно хотите уволить {sv_name}?'),
                False: Multi(
                    Format('Вы не можете уволить супервайзера {sv_name}.'),
                    Const(' '),
                    Const('За супервайзером все ещё закреплены магазины или сотрудники, а именно:'),
                    Format('Магазинов - {shops_count}'),
                    Format('Сотрудников - {seller_count}'),
                    Const(' '),
                    Const('Передайте сперва все магазины и сотрудников другому супервайзеру, затем сможете уволить'),
                ),
            },
            selector='some_thing'
        ),
        Button(Const('🔥 Уволить'), when='some_thing', id='confirm_fire_supervisor', on_click=selected.fire_confirm),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад'))
        ),
        getter=getters.fire_confirm,
        state=states.FireSvDirector.fire_confirm
    )

