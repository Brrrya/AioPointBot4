from aiogram import F

from aiogram_dialog import Window, DialogManager, Data

from aiogram_dialog.widgets.text import Format, Const, List, Multi, Case
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media.static import ContentType
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia


from dialogs.director_dialogs.main_message_dialog import (
    getters, keyboards, selected, states
)


async def director_main_message():
    return Window(
        Format('{main_message_text}'),
        keyboards.main_message,
        getter=getters.main_message,
        state=states.MainMessageDirector.main_message
    )
