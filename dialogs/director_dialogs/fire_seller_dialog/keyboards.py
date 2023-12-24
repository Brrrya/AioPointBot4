import operator

from aiogram_dialog.widgets.kbd import Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def choice_seller(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='dr_scroll_sellers_for_fire',
            item_id_getter=operator.itemgetter(1),
            items='sellers',
            on_click=on_click
        ),
        id='dr_all_sellers_scroll_for_fire',
        width=2,
        height=5
    )
