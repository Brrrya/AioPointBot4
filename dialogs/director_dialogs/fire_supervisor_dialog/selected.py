import logging

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.director_dialogs.fire_supervisor_dialog import states

from database.requests.director_requests import DirectorRequests


async def fire_choice_sv(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал супервайзера для увольнения - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(fire_sv_tgid=int(item_id))

    await manager.switch_to(states.FireSvDirector.fire_confirm)


async def fire_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Подтвердил увольнение СВ id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    await DirectorRequests.fire_sv(ctx.dialog_data.get('fire_sv_tgid'))

    await c.answer('Выполнено!')
    await manager.done()
