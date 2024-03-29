import logging
from datetime import date

from aiogram_dialog import Window, DialogManager, Data
from aiogram_dialog.widgets.kbd import Back, Button, Calendar, CalendarConfig
from aiogram_dialog.widgets.text import Format, Const, List, Multi, Case

from dialogs.supervisor_dialogs.main_message_dialog import (
    getters, keyboards, selected, states
)


async def on_process_result(data: Data, result: dict, manager: DialogManager, **kwargs):
    logging.info(f'on_process_result Supervisor result={result}'
                 f' id={manager.event.from_user.id} username={manager.event.from_user.username}')

    if result:
        switch_to = result.get('switch_to')
        if switch_to == 'main_message':
            await manager.switch_to(states.MainMessageSupervisor.main_message)
        elif switch_to == 'end':
            await manager.close_manager()


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
                True: Const("У вас нет ни одного магазина")
            },
            selector='no_shops'
        ),
        keyboards.main_message_kb(
            open_photo=selected.open_photos,
            rotate_photo=selected.rotate_photos,
            refresh_main_message=selected.refresh_main_message,
            change_structure=selected.change_structure,
            close_reports=selected.close_reports,
            close_reports_not_today=selected.close_reports_not_today,
            fridges_on=selected.fridge_on_photos,
            fridges_off=selected.fridge_off_photos,
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
        Button(Const('🔄 Обновить'), id='take_open_photos_sv', on_click=selected.open_photos),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
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
        Button(Const('🔄 Обновить'), id='take_rotate_photos_sv', on_click=selected.rotate_photos),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.rotate_photos,
        state=states.MainMessageSupervisor.rotate_photos
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
        state=states.MainMessageSupervisor.fridge_on_photos
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
        state=states.MainMessageSupervisor.fridge_off_photos
    )


async def close_reports():
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
        Button(Const('🔄 Обновить'), id='take_close_report_sv', on_click=selected.close_reports),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.close_reports,
        state=states.MainMessageSupervisor.close_reports,
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
        Button(Const('⬅️ Назад'), on_click=selected.back_to_main_message, id='back_to_main_message_sv'),
        getter=getters.structure_changes,
        state=states.MainMessageSupervisor.structure_changes
    )


async def checkers():
    return Window(
        Case(
            {
                True: List(
                    Multi(
                        Format('Магазин - {item[0]}'),
                        Format('Открытие - {item[1]}'),
                        Format('Ротации - {item[2]}'),
                        Const(' '),
                    ),
                    items='checkers'
                ),
                False: Const("У вас нет ни одного магазина")
            },
            selector='some_shops'
        ),

        Button(Const('🔧 Изменить проверяющих'), id='change_checker', on_click=selected.change_checker),
        Back(Const('⬅️ Назад')),
        getter=getters.checkers,
        state=states.MainMessageSupervisor.checkers
    )


async def close_reports_not_today():
    return Window(
        Const("За какой день показать отчеты?"),
        keyboards.calendar_for_reports(selected.close_reports_not_today_show),
        Button(Const('⬅️ Назад'), id='back_to_main_message_sv', on_click=selected.back_to_main_message),
        getter=getters.close_reports_not_today,
        state=states.MainMessageSupervisor.close_reports_not_today
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
        state=states.MainMessageSupervisor.close_reports_not_today_show,
    )

