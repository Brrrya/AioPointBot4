import logging

from aiogram.types import CallbackQuery
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.api.entities import ShowMode

from dialogs.director_dialogs.inspect_sv_dialog import states

from database.requests.director_requests import DirectorRequests
from database.requests.supervisor_requests import SupervisorRequests


async def back_to_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Инспекция | Вернулся к главному сообщению по кнопке id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states.InspectSupervisorDirector.main_message)


async def open_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Инспекция | Нажал кнопку фото открытия id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    all_photos = await SupervisorRequests.take_all_photo_rotate_or_state(ctx.start_data.get('dr_inspected_sv'), 'open')
    for photo in all_photos:
        await c.message.answer_photo(photo=photo[0], caption=photo[1])
    await manager.switch_to(states.InspectSupervisorDirector.open_photos, show_mode=ShowMode.SEND)


async def rotate_photos(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Инспекция | Нажал кнопку фото ротаций id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()
    all_photos = await SupervisorRequests.take_all_photo_rotate_or_state(ctx.start_data.get('dr_inspected_sv'), 'rotate')
    for photo in all_photos:
        await c.message.answer_photo(photo=photo[0], caption=photo[1])
    await manager.switch_to(states.InspectSupervisorDirector.rotate_photo, show_mode=ShowMode.SEND)


async def refresh_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Инспекция | Нажал кнопку обновить сообщение id={c.from_user.id} username={c.from_user.username}')


async def close_reports(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Директор | Инспекция | Нажал кнопку отчетов закрытия id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    all_data = await SupervisorRequests.take_all_close_report_data(ctx.start_data.get('dr_inspected_sv'))
    reports = all_data.get('reports')
    keys = reports.keys()
    for key in keys:
        text = ''
        text += f'Магазин - {reports[key]["shop_name"]}\n'
        text += f'Сотрудник - {reports[key]["seller_name"]}\n'
        text += f'РТО - {reports[key]["rto"]} / {reports[key]["p_rto"]}\n'
        text += f'ЦКП - {reports[key]["ckp"]} / {reports[key]["p_ckp"]}\n'
        text += f'Чеки - {reports[key]["check"]} / {reports[key]["p_check"]}\n'
        text += f'Дисконт. карты - {reports[key]["dcart"]}\n'

        media = MediaGroupBuilder()
        for photo in reports[key]['photos']:
            media.add_photo(photo)

        await c.message.answer(text)
        await c.message.answer_media_group(media.build())

    ctx.dialog_data.update(who_not_send_report=all_data.get('who_not_send'))

    await manager.switch_to(state=states.InspectSupervisorDirector.close_reports, show_mode=ShowMode.SEND)

