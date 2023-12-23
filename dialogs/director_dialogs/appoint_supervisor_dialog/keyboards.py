import operator

from aiogram_dialog.widgets.kbd import Back, Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def choice_new_sv(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='dr_scroll_sellers',
            item_id_getter=operator.itemgetter(1),
            items='sellers',
            on_click=on_click
        ),
        id='dr_all_sellers_scroll',
        width=2,
        height=5
    )

