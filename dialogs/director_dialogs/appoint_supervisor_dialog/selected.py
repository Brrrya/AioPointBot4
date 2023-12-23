import logging

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from dialogs.director_dialogs.appoint_supervisor_dialog import states
from dialogs.supervisor_dialogs.main_message_dialog import states as sv_states

from database.requests.director_requests import DirectorRequests


async def choice_new_sv(c: CallbackQuery, widget, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал сотрудника для повышения до СВ - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(appoint_sv=int(item_id))

    await manager.switch_to(states.AppointSvDirector.confirm)


async def confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Подтвердил повышение сотрудника id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    res = await DirectorRequests.appoint_supervisor(int(ctx.dialog_data.get('appoint_sv')))

    if res['was_authorized'] is True:
        """Если был где-то авторизирован обновляем сообщение того магазина"""
        await manager.bg(res['where_was_authorized_tgid'], res['where_was_authorized_tgid']).update(data={})

    await manager.bg(int(ctx.dialog_data.get('appoint_sv')), int(ctx.dialog_data.get('appoint_sv'))).start(mode=StartMode.RESET_STACK, state=sv_states.MainMessageSupervisor.main_message)

    await c.answer('Выполнено')
    await manager.done()

