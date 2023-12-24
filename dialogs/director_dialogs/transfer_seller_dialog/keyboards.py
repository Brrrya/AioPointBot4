import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format


def choice_seller(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='dr_scroll_sellers_for_transfer',
            item_id_getter=operator.itemgetter(1),
            items='sellers',
            on_click=on_click
        ),
        id='dr_all_sellers_scroll_for_transfer',
        width=2,
        height=5
    )


def choice_sv(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='dr_scroll_sv_for_transfer_his_sellers',
            item_id_getter=operator.itemgetter(1),
            items='supervisors',
            on_click=on_click
        ),
        id='dr_all_sv_scroll_for_transfer_his_sellers',
        width=2,
        height=4
    )

