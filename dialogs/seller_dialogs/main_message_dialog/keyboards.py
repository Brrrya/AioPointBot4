from aiogram_dialog.widgets.kbd import Group, Button, Row
from aiogram_dialog.widgets.text import Const


def main_message_kb(open_shop, close_shop, rotate_shop):
    return Group(
        Row(
            Button(Const('🔑 Открыть'), on_click=open_shop, id='open_shop'),
            Button(Const('📱 Ротации'), on_click=rotate_shop, id='rotate_shop'),
            ),
        Row(
            Button(Const('🔒 Закрыть'), on_click=close_shop, id='close_shop'),
        ),

        id='seller_main_message_group',
    )


