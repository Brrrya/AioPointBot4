import logging

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.api.entities import ShowMode

from dialogs.director_dialogs.main_message_dialog import states
from dialogs.director_dialogs.appoint_supervisor_dialog import states as states_appoint
from dialogs.director_dialogs.fire_supervisor_dialog import states as states_fire_sv
from dialogs.director_dialogs.fire_seller_dialog import states as states_fire_seller
from dialogs.director_dialogs.transfer_seller_dialog import states as states_transfer_seller
from dialogs.director_dialogs.transfer_shop_dialog import states as states_transfer_shop
from dialogs.director_dialogs.inspect_sv_dialog import states as states_inspect_sv

from database.requests.director_requests import DirectorRequests


async def back_to_main_window(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку вернуться к основному окну id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states.MainMessageDirector.main_message)


async def refresh(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку обновления основного окна id={c.from_user.id} username={c.from_user.username}')


async def structure_changes(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку изменения структуры id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states.MainMessageDirector.structure_changes)


async def appoint_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку назначить СВ id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_appoint.AppointSvDirector.choice_new_sv)


async def fire_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку уволить СВ id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_fire_sv.FireSvDirector.fire_choice_sv)


async def fire_seller(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку уволить продавца id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_fire_seller.FireSellerDirector.fire_choice_seller)


async def transfer_seller(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку передать сотрудника id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_transfer_seller.TransferSellerDirector.select_seller)


async def transfer_shop(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку передать магазин id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_transfer_shop.TransferShopDirector.select_shop)


async def inspected_sv(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Нажал кнопку инспектировать СВ id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states.MainMessageDirector.inspect_sv)


async def start_inspect(c: CallbackQuery, widget, manager: DialogManager, item_id: str):
    logging.info(f'Директор | Выбрал кого инспектировать - {item_id} СВ id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_inspect_sv.InspectSupervisorDirector.main_message,
                        data={'dr_inspected_sv': int(item_id)})
