import logging

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.director_dialogs.main_message_dialog import states
from dialogs.director_dialogs.appoint_supervisor_dialog import states as states_appoint
from dialogs.director_dialogs.fire_supervisor_dialog import states as states_fire_sv

from database.requests.supervisor_requests import SupervisorRequests


async def refresh(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку обновления основного окна id={c.from_user.id} username={c.from_user.username}')

    await manager.update(data={})


async def structure_changes(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку изменения структуры id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states.MainMessageDirector.structure_changes)


async def inspected_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    pass


async def appoint_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку назначить СВ id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_appoint.AppointSvDirector.choice_new_sv)


async def fire_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку уволить СВ id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_fire_sv.FireSvDirector.fire_choice_sv)



