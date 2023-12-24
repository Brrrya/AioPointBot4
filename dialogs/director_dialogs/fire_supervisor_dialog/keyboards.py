import operator

from aiogram_dialog.widgets.kbd import Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def choice_sv(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='dr_scroll_supervisors',
            item_id_getter=operator.itemgetter(1),
            items='supervisors',
            on_click=on_click
        ),
        id='dr_all_supervisors_scroll',
        width=2,
        height=4
    )
