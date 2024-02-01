import operator
from datetime import date

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Group, Button, Row, Calendar, CalendarConfig
from aiogram_dialog.widgets.text import Format, Const


def main_message_kb(
        open_photo,
        rotate_photo,
        refresh_main_message,
        close_reports,
        close_reports_not_today
):
    return Group(
        Button(Const('🔄 Обновить'), id='dr_sv_main_message_refresh', on_click=refresh_main_message),
        Row(
            Button(Const('🔐 Чеки открытия'), id='dr_sv_main_message_open', on_click=open_photo),
            Button(Const('📱 Фото ротаций'), id='dr_sv_main_message_rotate', on_click=rotate_photo),
        ),
        Button(Const('📒 Отчеты закрытия за сегодня'), id='dr_close_reports', on_click=close_reports),
        Button(Const('🗄 Отчеты закрытия за предыдущие дни'), id='dr_close_reports_for_other_day', on_click=close_reports_not_today),

        id='dr_inspect_supervisor',
    )


def calendar_for_reports(on_click):
    cal = Calendar(
        id='calendar_for_change_plan_',
        on_click=on_click
    )
    return cal
