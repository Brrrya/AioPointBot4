import logging

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from dialogs.director_dialogs.fire_seller_dialog import states
from dialogs.seller_dialogs.main_message_dialog import states as states_seller

from database.requests.director_requests import DirectorRequests


async def fire_choice_seller(c: CallbackQuery, widget: Button, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал продавца для увольнения - {item_id} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(fire_seller_tgid=int(item_id))

    await manager.switch_to(states.FireSellerDirector.fire_confirm)


async def fire_seller_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Подтвердил увольнение продавца id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    data = await DirectorRequests.fire_seller(int(ctx.dialog_data.get('fire_seller_tgid')))

    if data['was_authorized'] is True:
        """Если был где-то авторизирован обновляем сообщение того магазина"""
        await manager.bg(data['where_was_authorized_tgid'], data['where_was_authorized_tgid']).update(data={})

    await manager.bg(int(ctx.dialog_data.get('fire_seller_tgid')), int(ctx.dialog_data.get('fire_seller_tgid'))).start(mode=StartMode.RESET_STACK, state=states_seller.MainMessageUser.plug)


    await c.answer('Выполнено!')
    await manager.done()
