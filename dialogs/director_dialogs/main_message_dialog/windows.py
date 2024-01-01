from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const

from dialogs.director_dialogs.main_message_dialog import (
    getters, keyboards, selected, states
)


async def director_main_message():
    return Window(
        Format('{main_message_text}'),
        Button(Const('🔄 Обновить'), on_click=selected.refresh, id='refresh_main_message_dr'),
        Button(Const('🔦 Инспектировать СВ'), on_click=selected.inspected_sv, id='dr_inspect_sv'),
        Button(Const('⚙️ Изменить структуру'), on_click=selected.structure_changes, id='structure_changes_main_message_dr'),
        # Button(
        #     Const('Админ команды'),
        #     id='admin_commands',
        #     on_click=selected.admin_commands,
        #     when='is_admin'
        # ),
        getter=getters.main_message,
        state=states.MainMessageDirector.main_message
    )


async def structure_changes():
    return Window(
        Const('Окно изменения структуры сети'),
        keyboards.main_message(
            appoint_sv=selected.appoint_sv,
            fire_sv=selected.fire_sv,
            transfer_shop=selected.transfer_shop,
            transfer_seller=selected.transfer_seller,
            fire_seller=selected.fire_seller,
        ),
        getter=getters.structure_changes,
        state=states.MainMessageDirector.structure_changes
    )


async def who_will_inspected():
    return Window(
        Const("Выберете управляющего для просмотра"),
        keyboards.who_will_inspected(on_click=selected.start_inspect),
        Button(Const('⬅️ Назад'), id='dr_back_to_main_window', on_click=selected.back_to_main_window),
        getter=getters.who_will_inspected,
        state=states.MainMessageDirector.inspect_sv

    )
