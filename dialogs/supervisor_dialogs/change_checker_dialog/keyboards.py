import operator

from aiogram_dialog.widgets.kbd import Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def select_shop_checker(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='s_scroll_shops_checkers',
            item_id_getter=operator.itemgetter(1),
            items='shops',
            on_click=on_click
        ),
        id='all_shop_scroll_checkers',
        width=2,
        height=4
    )

def select_seller_checker(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='s_scroll_seller_checkers',
            item_id_getter=operator.itemgetter(1),
            items='sellers',
            on_click=on_click
        ),
        id='all_seller_scroll_checkers',
        width=2,
        height=4
    )


