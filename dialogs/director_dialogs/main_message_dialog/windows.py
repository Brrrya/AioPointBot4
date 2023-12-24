from aiogram import F

from aiogram_dialog import Window, DialogManager, Data

from aiogram_dialog.widgets.text import Format, Const, List, Multi, Case
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media.static import ContentType
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia


from dialogs.director_dialogs.main_message_dialog import (
    getters, keyboards, selected, states
)


async def director_main_message():
    return Window(
        Format('{main_message_text}'),
        Button(Const('Обновить'), on_click=selected.refresh, id='refresh_main_message_dr'),
        Button(Const('Инспектировать СВ'), on_click=selected.inspected_sv, id='dr_inspect_sv'),
        Button(Const('Изменить структуру'), on_click=selected.structure_changes, id='structure_changes_main_message_dr'),
        getter=getters.main_message,
        state=states.MainMessageDirector.main_message
    )


async def structure_changes():
    return Window(
        Const('Окно изменения структуры сети'),
        keyboards.main_message(
            appoint_sv=selected.appoint_sv,
            fire_sv=selected.fire_sv,
            transfer_shop=None,
            transfer_seller=None,
            fire_seller=selected.fire_seller,
        ),
        getter=getters.structure_changes,
        state=states.MainMessageDirector.structure_changes
    )


