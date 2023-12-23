import operator

from aiogram_dialog.widgets.kbd import Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def main_message(refresh, appoint_sv, fire_sv, inspect_sv):
    return Group(
        Button(Const('Обновить'), on_click=refresh, id='refresh_main_message_dr'),
        Row(
            Button(Const('Назначить СВ'), on_click=appoint_sv, id='appoint_sv'),
            Button(Const('Уволить СВ'), on_click=fire_sv, id='fire_sv'),
        ),
        Button(Const('Инспектировать'), on_click=inspect_sv, id='inspect_sv'),

        id='seller_main_message_group',
    )
