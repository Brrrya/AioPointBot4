from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Format, Const, Case, Multi, List

from dialogs.director_dialogs.inspect_sv_dialog import (
    getters, keyboards, selected, states
)


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
                True: Const("У супервайзера нет ни одного магазина")
            },
            selector='no_shops'
        ),
        keyboards.main_message_kb(
            open_photo=selected.open_photos,
            rotate_photo=selected.rotate_photos,
            refresh_main_message=selected.refresh_main_message,
            close_reports=selected.close_reports
        ),
        Cancel(Const("❌ Отмена")),
        getter=getters.main_message,
        state=states.InspectSupervisorDirector.main_message,
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
        Button(Const('🔄 Обновить'), id='take_open_photos_sv', on_click=selected.open_photos),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.open_photos,
        state=states.InspectSupervisorDirector.open_photos
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
        Button(Const('🔄 Обновить'), id='take_rotate_photos_sv', on_click=selected.rotate_photos),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.rotate_photos,
        state=states.InspectSupervisorDirector.rotate_photo
    )


async def close_reports():
    return Window(
        Case(
            {
                True: Const('Все магазины отправили вечерний отчет!'),
                False: Multi(
                    Const('Ещё не отправили отчёт:'),
                    List(
                        Format('{item[0]}'),
                        items='all_not_close_report'
                    )
                )
            },
            selector='close_report_or_not'
        ),
        Button(Const('🔄 Обновить'), id='take_close_report_sv', on_click=selected.close_reports),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.close_reports,
        state=states.InspectSupervisorDirector.close_reports,
    )

