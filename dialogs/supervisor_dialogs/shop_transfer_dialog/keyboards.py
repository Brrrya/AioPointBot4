import operator

from aiogram_dialog.widgets.kbd import Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def all_shops_by_sv(shop_choice):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='scrolling_shop_transfer',
            item_id_getter=operator.itemgetter(1),
            items='shops_list',
            on_click=shop_choice
        ),
        id='all_shop_scroll_transfer',
        width=2,
        height=4
    )


def all_sv_for_transfer(sv_choice):
    return ScrollingGroup(
            Select(
                Format('{item[0]}'),
                id='scrolling_sellers',
                item_id_getter=operator.itemgetter(1),
                items='supervisors',
                on_click=sv_choice
            ),
            id='all_supervisors_scroll_for_transfer',
            width=1,
            height=4
    )
