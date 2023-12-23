import asyncio
import logging

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests


async def choice_new_sv(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.appoint_sv.main_message>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_workers()

    return {
        'sellers': data
    }


async def confirm(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.appoint_sv.confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()
    data = await DirectorRequests.select_data_about_seller(ctx.dialog_data.get('appoint_sv'))

    return {
        'seller_name': data['full_name']
    }

