import calendar
from datetime import date, datetime

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Calendar, CalendarConfig
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
                            Format(' Состояние ХО - {item[4]}'),
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
            close_reports=selected.close_reports,
            close_reports_not_today=selected.close_reports_not_today,
            fridges_on=selected.fridge_on_photos,
            fridges_off=selected.fridge_off_photos,
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


async def fridges_on_photos():
    return Window(
        Case(
            {
                True: Const('Все холодильники включены!'),
                False: Multi(
                    Const('Не включили ХО ещё:'),
                    List(
                        Format('{item[0]}'),
                        items='all_not_fridge_on'
                    )
                )
            },
            selector='fridge_on_or_off'
        ),
        Button(Const('🔄 Обновить'), id='take_fridge_on_photos_sv', on_click=selected.fridge_on_photos),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.fridges_on_photos,
        state=states.InspectSupervisorDirector.fridge_on_photos
    )


async def fridges_off_photos():
    return Window(
        Case(
            {
                True: Const('Все холодильники выключены!'),
                False: Multi(
                    Const('Не выключили ХО ещё:'),
                    List(
                        Format('{item[0]}'),
                        items='all_not_fridge_off'
                    )
                )
            },
            selector='fridge_off_or_on'
        ),
        Button(Const('🔄 Обновить'), id='take_fridge_off_photos_sv', on_click=selected.fridge_off_photos),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.fridges_off_photos,
        state=states.InspectSupervisorDirector.fridge_off_photos
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


async def close_reports_not_today():
    return Window(
        Const("За какой день показать отчеты?"),
        keyboards.calendar_for_reports(selected.close_reports_not_today_show),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.close_reports_not_today,
        state=states.InspectSupervisorDirector.close_reports_not_today
    )


async def close_reports_not_today_show():
    return Window(
        Case(
            {
                True: Const('Все магазины отправили вечерний отчет!'),
                False: Multi(
                    Const('Не отправили отчёт:'),
                    List(
                        Format('{item[0]}'),
                        items='all_not_close_report'
                    )
                )
            },
            selector='close_report_or_not'
        ),
        Button(Const('🗄 Другая дата'), id='other_date_report_dr', on_click=selected.close_reports_not_today),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.close_reports,
        state=states.InspectSupervisorDirector.close_reports_not_today_show,
    )

