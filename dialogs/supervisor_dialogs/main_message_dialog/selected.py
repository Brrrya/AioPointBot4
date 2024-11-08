import logging
from datetime import datetime

from aiogram.utils.media_group import MediaGroupBuilder

from aiogram.types import CallbackQuery

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.api.entities import ShowMode

from dialogs.supervisor_dialogs.main_message_dialog import states as states_main_message
from dialogs.supervisor_dialogs.seller_transfer_dialog import states as states_transfer_seller
from dialogs.supervisor_dialogs.shop_transfer_dialog import states as states_transfer_shop
from dialogs.supervisor_dialogs.fire_seller_dialog import states as states_fire_seller
from dialogs.supervisor_dialogs.change_checker_dialog import states as states_change_open_checker


from database.requests.supervisor_requests import SupervisorRequests


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
    await manager.switch_to(state=states_main_message.MainMessageSupervisor.open_photos, show_mode=ShowMode.SEND)


async def rotate_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку получения фото ротаций id={c.from_user.id} username={c.from_user.username}')

    all_photos = await SupervisorRequests.take_all_photo_rotate_or_state(sv_tgid=int(c.from_user.id),
                                                                         action='rotate')
    for photo in all_photos:
        await c.message.answer_photo(photo=photo[0], caption=photo[1])
    await manager.switch_to(state=states_main_message.MainMessageSupervisor.rotate_photos, show_mode=ShowMode.SEND)


async def fridge_on_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку получения фото вкл ХО id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    all_data = await SupervisorRequests.take_fridges_photos(int(c.from_user.id), photos_action=True)
    reports = all_data.get('reports')
    keys = reports.keys()
    for key in keys:
        text = reports[key]["shop_name"]

        media = MediaGroupBuilder()
        for photo in reports[key]['photos']:
            media.add_photo(photo)

        await c.message.answer(text)
        await c.message.answer_media_group(media.build())

    ctx.dialog_data.update(who_not_fridge_on=all_data.get('who_not_send'))

    await manager.switch_to(state=states_main_message.MainMessageSupervisor.fridge_on_photos, show_mode=ShowMode.SEND)


async def fridge_off_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку получения фото выкл ХО id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    all_data = await SupervisorRequests.take_fridges_photos(int(c.from_user.id), photos_action=False)
    reports = all_data.get('reports')
    keys = reports.keys()
    for key in keys:
        text = reports[key]["shop_name"]

        media = MediaGroupBuilder()
        for photo in reports[key]['photos']:
            media.add_photo(photo)

        await c.message.answer(text)

        if reports[key]['photos']:
            await c.message.answer_media_group(media.build())
        else:
            await c.message.answer_photo('https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637')

    ctx.dialog_data.update(who_not_fridge_off=all_data.get('who_not_send'))

    await manager.switch_to(state=states_main_message.MainMessageSupervisor.fridge_off_photos, show_mode=ShowMode.SEND)


async def close_reports(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку получения отчетов закрытия id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    all_data = await SupervisorRequests.take_all_close_report_data(int(c.from_user.id))
    reports = all_data.get('reports')
    keys = reports.keys()
    for key in keys:
        text = ''
        text += f'Магазин - {reports[key]["shop_name"]}\n'
        text += f'Сотрудник - {reports[key]["seller_name"]}\n'
        text += f'РТО - {reports[key]["rto"]} / {reports[key]["p_rto"]}\n'
        # text += f'ЦКП - {reports[key]["ckp"]} / {reports[key]["p_ckp"]}\n'
        text += f'Чеки - {reports[key]["check"]} / {reports[key]["p_check"]}\n'
        # text += f'Дисконт. карты - {reports[key]["dcart"]}\n'

        media = MediaGroupBuilder()
        for photo in reports[key]['photos']:
            media.add_photo(photo)

        await c.message.answer(text)
        await c.message.answer_media_group(media.build())

    ctx.dialog_data.update(who_not_send_report=all_data.get('who_not_send'))

    await manager.switch_to(state=states_main_message.MainMessageSupervisor.close_reports, show_mode=ShowMode.SEND)


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


async def close_reports_not_today(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'СВ | Нажал кнопку отчетов закрытия за другой день id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(state=states_main_message.MainMessageSupervisor.close_reports_not_today)


async def close_reports_not_today_show(c: CallbackQuery, widget, manager: DialogManager, select_date: datetime.date):
    logging.info(f'СВ | Выбрал день для просмотра отчетов - {select_date} id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    all_data = await SupervisorRequests.take_all_close_report_data(c.from_user.id, select_date)
    reports = all_data.get('reports')
    keys = reports.keys()
    for key in keys:
        text = ''
        text += f'Магазин - {reports[key]["shop_name"]}\n'
        text += f'Сотрудник - {reports[key]["seller_name"]}\n'
        text += f'РТО - {reports[key]["rto"]} / {reports[key]["p_rto"]}\n'
        # text += f'ЦКП - {reports[key]["ckp"]} / {reports[key]["p_ckp"]}\n'
        text += f'Чеки - {reports[key]["check"]} / {reports[key]["p_check"]}\n'
        # text += f'Дисконт. карты - {reports[key]["dcart"]}\n'

        media = MediaGroupBuilder()
        for photo in reports[key]['photos']:
            media.add_photo(photo)

        await c.message.answer(text)
        await c.message.answer_media_group(media.build())

    ctx.dialog_data.update(who_not_send_report=all_data.get('who_not_send'))

    await manager.switch_to(state=states_main_message.MainMessageSupervisor.close_reports_not_today_show, show_mode=ShowMode.SEND)

