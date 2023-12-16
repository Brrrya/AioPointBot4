from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.input import MessageInput

from aiogram_dialog.widgets.kbd import Cancel

from loguru import logger

from dialogs.shop_dialogs.main_message_dialog import (
    getters, keyboards, selected, states
)


async def main_message():
    return Window(
        Format("Магазин - {title}"),
        Format("Работник - {worker}"),
        Format("Управляющий - {supervisor}"),
        Format("Магазин - {open_or_not}"),
        Format("Ротации - {rotate_or_not}"),
        keyboards.main_message_kb(
            auth=selected.go_to_authorization,
            register=selected.go_to_registration,
            update_plan=selected.go_to_update_plan,
            get_plan=selected.get_plan,
            change_plan=selected.change_plan_button,

        ),
        getter=getters.main_message,
        state=states.MainMessage.main_message,
    )


async def authorization():
    return Window(
        Const("Сканируйте свой бейджик"),
        MessageInput(selected.take_auth_badge),
        Back(Const('❌ Отмена')),
        state=states.MainMessage.auth_wait_badge
    )

