import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Group, Button, Row
from aiogram_dialog.widgets.text import Format, Const


def main_message_kb(
        open_photo,
        rotate_photo,
        refresh_main_message,
        close_reports
):
    return Group(
        Button(Const('Обновить'), id='dr_sv_main_message_refresh', on_click=refresh_main_message),
        Row(
            Button(Const('Чеки открытия'), id='dr_sv_main_message_open', on_click=open_photo),
            Button(Const('Фото ротаций'), id='dr_sv_main_message_rotate', on_click=rotate_photo),
        ),
        Button(Const('Отчеты закрытия'), id='dr_close_reports', on_click=close_reports),

        id='dr_inspect_supervisor',
    )
