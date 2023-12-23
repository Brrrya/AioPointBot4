import operator

from aiogram_dialog.widgets.kbd import Back, Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def main_message(appoint_sv, fire_sv, inspect_sv):
    return Group(
        Row(
            Button(Const('Назначить СВ'), on_click=appoint_sv, id='dr_appoint_sv'),
            Button(Const('Уволить СВ'), on_click=fire_sv, id='dr_fire_sv'),
        ),
        Row(
            Button(Const('Передать магазин'), on_click=appoint_sv, id='dr_transfer_shop'),
            Button(Const('Передать продавца'), on_click=fire_sv, id='dr_transfer_seller'),
        ),
        Button(Const('Уволить продавца'), on_click=inspect_sv, id='dr_fire_seller'),
        Back(Const("<<< Назад")),
        id='seller_main_message_group',
    )
