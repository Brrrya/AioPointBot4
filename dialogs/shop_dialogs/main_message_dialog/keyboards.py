from aiogram_dialog.widgets.kbd import Group, Button, Row
from aiogram_dialog.widgets.text import Const


def main_message_kb(auth, register, update_plan, get_plan):
    return Group(
        Button(Const('🙋 Авторизация'), id='shop_main_message_auth', on_click=auth),
        Row(
            Button(Const('📊 Получить план'), id='shop_main_message_take_plan', on_click=get_plan),
            Button(Const('📝 Обновить план'), id='shop_main_message_update_plan', on_click=update_plan),
        ),
        Button(Const('🆕 Зарегистрировать нового сотрудника'), id='shop_main_message_register_new', on_click=register),
        id='shop_main_message_group',
    )


