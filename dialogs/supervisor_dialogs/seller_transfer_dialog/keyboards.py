import operator

from aiogram_dialog.widgets.kbd import Group, Button, Row, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format


def all_sellers_by_sv(seller_choice):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='scrolling_sellers',
            item_id_getter=operator.itemgetter(1),
            items='sellers_list',
            on_click=seller_choice
        ),
        id='all_sellers_scroll',
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
