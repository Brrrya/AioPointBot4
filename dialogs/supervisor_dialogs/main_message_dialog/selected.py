import asyncio
import logging

from aiogram.utils.media_group import MediaGroupBuilder, InputMediaPhoto

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.supervisor_dialogs.main_message_dialog import states as states_main_message
from dialogs.supervisor_dialogs.seller_transfer_dialog import states as states_transfer_seller
from dialogs.supervisor_dialogs.shop_transfer_dialog import states as states_transfer_shop
from dialogs.supervisor_dialogs.fire_seller_dialog import states as states_fire_seller
from dialogs.supervisor_dialogs.change_checker_dialog import states as states_change_open_checker


from database.supervisor_requests import SupervisorRequests


async def refresh_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Обновил главное сообщение id={c.from_user.id} username={c.from_user.username}')

    await manager.bg(c.from_user.id, c.from_user.id).update(data=manager.start_data)


async def back_to_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Вернулся к главному сообщению по кнопке id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states_main_message.MainMessageSupervisor.main_message)


async def open_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку получения фото открытия id={c.from_user.id} username={c.from_user.username}')

    all_photos = await SupervisorRequests.take_all_photo_rotate_or_state(int(c.from_user.id), 'open')
    for photo in all_photos:
        await c.message.answer_photo(photo=photo[0], caption=photo[1])
    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=states_main_message.MainMessageSupervisor.open_photos)


async def rotate_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку получения фото ротаций id={c.from_user.id} username={c.from_user.username}')

    all_photos = await SupervisorRequests.take_all_photo_rotate_or_state(sv_tgid=int(c.from_user.id),
                                                                         action='rotate')
    for photo in all_photos:
        await c.message.answer_photo(photo=photo[0], caption=photo[1])
    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=states_main_message.MainMessageSupervisor.rotate_photos)


async def close_reports(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку получения отчетов закрытия id={c.from_user.id} username={c.from_user.username}')

    all_data = await SupervisorRequests.take_all_close_report_data(int(c.from_user.id))
    keys = all_data.keys()
    for key in keys:
        text = ''
        text += f'Магазин - {all_data[key]["shop_name"]}\n'
        text += f'Сотрудник - {all_data[key]["seller_name"]}\n'
        text += f'РТО - {all_data[key]["rto"]}\n'
        text += f'ЦКП - {all_data[key]["ckp"]}\n'
        text += f'Чеки - {all_data[key]["check"]}\n'
        text += f'Дисконт. карты - {all_data[key]["dcart"]}\n'

        media = MediaGroupBuilder()
        for photo in all_data[key]['photos']:
            media.add_photo(photo)

        await c.message.answer(text)
        await c.message.answer_media_group(media.build())

    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=states_main_message.MainMessageSupervisor.close_reports)


async def change_structure(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку изменения структуры куста id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states_main_message.MainMessageSupervisor.structure_changes)


async def checkers(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку проверяющие id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states_main_message.MainMessageSupervisor.checkers)


async def transfer_seller(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку передачи сотрудника id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_transfer_seller.SellerTransferSupervisor.who_will_transfer)


async def transfer_shop(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку передачи магазина id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_transfer_shop.ShopTransferSupervisor.who_will_transfer_shop)


async def change_checker(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку проверяющих id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_change_open_checker.ChangeCheckerSupervisor.select_role)


async def fire_seller(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку удаления сотрудника id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_fire_seller.SellerFireSupervisor.who_will_fired)

