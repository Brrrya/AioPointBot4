import asyncio
import logging

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests


async def fire_choice_seller(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.fire_seller.fire_choice_seller>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_workers()

    return {
        'sellers': data
    }


async def fire_seller_confirm(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.fire_seller.fire_seller_confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    data = await DirectorRequests.select_data_about_seller(ctx.dialog_data.get('fire_seller_tgid'))

    return data
