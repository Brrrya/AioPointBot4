from aiogram import F

from aiogram_dialog import Window, DialogManager, Data

from aiogram_dialog.widgets.text import Format, Const, List, Multi, Case
from aiogram_dialog.widgets.kbd import Back, Button, Cancel
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media.static import ContentType
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia


from dialogs.supervisor_dialogs.main_message_dialog import (
    getters, keyboards, selected, states
)


async def on_process_result(data: Data, result: dict, manager: DialogManager, **kwargs):
    if result:
        switch_to = result.get('switch_to')
        if switch_to == 'main_message':
            await manager.switch_to(states.MainMessageSupervisor.main_message)


async def main_message():
    return Window(
        Case(
            {
                False: List(
                        Multi(
                            Format('🏢 {item[0]}'),
                            Format(' Сотрудник - {item[1]}'),
                            Format(' Магазин - {item[2]}'),
                            Format(' Ротации - {item[3]}'),
                            Const(' ')
                        ),
                        items='shops_data',
                    ),
                True: Const("У вас нет ни одного магазина")
            },
            selector='no_shops'
        ),
        keyboards.main_message_kb(
            open_photo=selected.open_photos,
            rotate_photo=selected.rotate_photos,
            refresh_main_message=selected.refresh_main_message,
            change_structure=selected.change_structure
        ),

        getter=getters.main_message,
        state=states.MainMessageSupervisor.main_message,
    )


async def open_photos():
    return Window(
        Case(
            {
                True: Const('Все магазины открыты!'),
                False: Multi(
                    Const('Не открылись ещё:'),
                    List(
                        Format('{item[0]}'),
                        items='all_not_open'
                    )
                )
            },
            selector='open_or_not'
        ),
        Button(Const('Обновить'), id='take_open_photos_sv', on_click=selected.open_photos),
        Button(Const('Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.open_photos,
        state=states.MainMessageSupervisor.open_photos
    )


async def rotate_photos():
    return Window(
        Case(
            {
                True: Const('Все магазины сделали ротации!'),
                False: Multi(
                    Const('Не сделали ротации ещё:'),
                    List(
                        Format('{item[0]}'),
                        items='all_not_rotate'
                    )
                )
            },
            selector='rotate_or_not'
        ),
        Button(Const('Обновить'), id='take_rotate_photos_sv', on_click=selected.rotate_photos),
        Button(Const('Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.rotate_photos,
        state=states.MainMessageSupervisor.rotate_photos
    )


async def structure_changes():
    return Window(
        Const("Окно для изменения структуры в кусте"),
        keyboards.structure_changes_kb(
            checkers=selected.checkers,
            fire_seller=selected.fire_seller,
            transfer_seller=selected.transfer_seller,
            transfer_shop=selected.transfer_shop,
        ),
        Button(Const('Назад'), on_click=selected.back_to_main_message, id='back_to_main_message_sv'),
        state=states.MainMessageSupervisor.structure_changes
    )


