import logging

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.director_dialogs.main_message_dialog import states

from database.requests.supervisor_requests import SupervisorRequests


async def refresh(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку обновления основного окна id={c.from_user.id} username={c.from_user.username}')

    await manager.update(data={})


async def fire_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку уволить СВ id={c.from_user.id} username={c.from_user.username}')




