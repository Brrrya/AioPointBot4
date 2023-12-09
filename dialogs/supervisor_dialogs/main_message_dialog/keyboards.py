from aiogram_dialog.widgets.kbd import Group, Button, Row
from aiogram_dialog.widgets.text import Const


def main_message_kb(
        open_photo, rotate_photo,  refresh_main_message, change_structure
):
    return Group(
        Button(Const('Обновить'), id='sv_main_message_refresh', on_click=refresh_main_message),
        Row(
            Button(Const('Чеки открытия'), id='sv_main_message_open', on_click=open_photo),
            Button(Const('Фото ротаций'), id='sv_main_message_rotate', on_click=rotate_photo),
        ),
        Button(Const('Изменить структуру'), id='sv_main_message_change_structure', on_click=change_structure),

        id='shop_main_message_group',
    )

def structure_changes_kb(
        checkers,
        fire_seller,
        transfer_seller,
        transfer_shop,
):
    return Group(
        Button(Const('Проверяющие'), id='sv_main_message_change_checker', on_click=checkers),
        Button(Const('Передать сотрудника'), id='sv_main_message_transfer_seller', on_click=transfer_seller),
        Button(Const('Передать магазин'), id='sv_main_message_transfer_shop', on_click=transfer_shop),
        Button(Const('Удалить сотрудника'), id='sv_main_message_dell_seller', on_click=fire_seller),

    )


