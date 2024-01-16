import logging

from aiogram import F
from aiogram_dialog import Window, DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.media.static import ContentType
from aiogram_dialog.widgets.text import Format, Const

import commands.register
from dialogs.seller_dialogs.main_message_dialog import (
    getters, keyboards, selected, states
)


async def on_process_result(data: Data, result: dict, manager: DialogManager, **kwargs):
    logging.info(f'on_process_result Seller result = {result}')
    if result:
        switch_to = result.get('switch_to')
        if switch_to == 'plug':
            await manager.switch_to(states.MainMessageUser.plug)
        elif switch_to == 'end':
            await manager.close_manager()


async def plug():
    return Window(
        Const("Вы не авторизированны ни на одном магазине"),
        MessageInput(selected.checker_command, content_types=ContentType.TEXT, filter=F.text.in_({'/open', '/rotate', '/close'})),
        MessageInput(selected.register_command, content_types=ContentType.TEXT, filter=F.text == '/register'),
        getter=getters.plug,
        state=states.MainMessageUser.plug
    )


async def register_command():
    return Window(
        Const("Введите код регистрации"),
        Button(Const('Назад'), on_click=selected.to_plug, id='pack_to_plug'),
        MessageInput(selected.register_command_code, content_types=ContentType.TEXT),
        getter=getters.register_command,
        state=states.MainMessageUser.register_command
    )


async def main_message():
    return Window(
        Format("Магазин - {title}"),
        Format("Работник - {worker}"),
        Format("Управляющий - {supervisor}"),
        Format("Магазин - {open_or_not}"),
        Format("Ротации - {rotate_or_not}"),
        MessageInput(selected.checker_command, content_types=ContentType.TEXT, filter=F.text.in_({'/open', '/rotate', '/close'})),
        keyboards.main_message_kb(
            open_shop=selected.open_button,
            rotate_shop=selected.rotate_button,
            close_shop=selected.close_button,
        ),
        getter=getters.main_message,
        state=states.MainMessageUser.main_message,
    )


async def open_photo():
    return Window(
        Const('Отправьте фотографию чека открытия'),
        Const('Только одну фотографию!'),
        MessageInput(func=selected.open_photo, content_types=ContentType.PHOTO),
        Button(Const('❌ Отмена'), on_click=selected.to_main_message, id='user_button_back_to_main_window'),
        getter=getters.open_photo_take,
        state=states.MainMessageUser.open_photo
    )


async def open_photo_confirm():
    return Window(
        DynamicMedia(selector='photo'),
        Const('Это верное фото?'),
        Button(Const("✅ Да"), on_click=selected.open_photo_confirm, id='user_open_photo_confirm'),
        Back(Const('⬅️ Нет')),
        getter=getters.open_photo_confirm,
        state=states.MainMessageUser.open_photo_confirm
    )


async def rotate_photo():
    return Window(
        Const('Отправьте фотографию сделанных ротаций'),
        Const('Только одну фотографию!'),
        MessageInput(func=selected.rotate_photo, content_types=ContentType.PHOTO),
        Button(Const('❌ Отмена'), on_click=selected.to_main_message, id='user_button_back_to_main_window'),
        getter=getters.rotate_photo_take,
        state=states.MainMessageUser.rotate_photo
    )


async def rotate_photo_confirm():
    return Window(
        DynamicMedia(selector='photo'),
        Const('Это верное фото?'),
        Button(Const("✅ Да"), on_click=selected.rotate_photo_confirm, id='user_rotate_photo_confirm'),
        Back(Const('⬅️ Нет')),
        getter=getters.rotate_photo_confirm,
        state=states.MainMessageUser.rotate_photo_confirm
    )

