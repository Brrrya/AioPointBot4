import operator
from datetime import date

from aiogram_dialog.widgets.kbd import Group, Button, Row, ScrollingGroup, Select, Calendar, CalendarConfig
from aiogram_dialog.widgets.text import Const, Format


def main_message_kb(
        open_photo,
        rotate_photo,
        refresh_main_message,
        change_structure,
        close_reports,
        close_reports_not_today,
        fridges_on,
        fridges_off
):
    return Group(
        Button(Const('🔄 Обновить'), id='sv_main_message_refresh', on_click=refresh_main_message),
        Row(
            Button(Const('🔐 Чеки открытия'), id='sv_main_message_open', on_click=open_photo),
            Button(Const('📱 Фото ротаций'), id='sv_main_message_rotate', on_click=rotate_photo),
        ),
        Row(
            Button(Const('🔐 Фото вкл ХО'), id='sv_main_message_fridges_on', on_click=fridges_on),
            Button(Const('📱 Фото выкл ХО'), id='sv_main_message_fridges_off', on_click=fridges_off),
        ),

        Button(Const('📒 Отчеты закрытия'), id='close_reports', on_click=close_reports),
        Button(Const('🗄 Отчеты закрытия за предыдущие дни'), id='dr_close_reports_for_other_day', on_click=close_reports_not_today),
        Button(Const('⚙️ Изменить структуру'), id='sv_main_message_change_structure', on_click=change_structure),

        id='shop_main_message_group',
    )

def structure_changes_kb(
        checkers,
        fire_seller,
        transfer_seller,
        transfer_shop,
):
    return Group(
        Button(Const('🔦 Проверяющие'), id='sv_main_message_change_checker', on_click=checkers),
        Button(Const('🧑 Передать сотрудника'), id='sv_main_message_transfer_seller', on_click=transfer_seller),
        Button(Const('🏢 Передать магазин'), id='sv_main_message_transfer_shop', on_click=transfer_shop),
        Button(Const('🔥 Удалить сотрудника'), id='sv_main_message_dell_seller', on_click=fire_seller),

    )


def calendar_for_reports(on_click):
    cal = Calendar(
        id='calendar_for_change_plan_',
        on_click=on_click
    )
    return cal

