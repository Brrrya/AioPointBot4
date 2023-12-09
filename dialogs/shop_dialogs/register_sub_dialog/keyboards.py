import operator

from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import ScrollingGroup, Select


def take_supervisor(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='s_scroll_supervisors',
            item_id_getter=operator.itemgetter(1),
            items='supervisors',
            on_click=on_click
        ),
        id='all_supervisors_scroll',
        width=2,
        height=4
    )
