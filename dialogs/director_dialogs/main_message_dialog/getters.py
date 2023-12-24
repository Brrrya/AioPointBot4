import asyncio
import logging

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests


async def main_message(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.main_message.main_message>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.main_message_info()

    text = 'Общие данные\n' \
           f'Всего управляющих - {data["sv_count"]}\n' \
           f'Всего продавцов - {data["seller_count"]}\n\n'


    for sv in data['sv_data']:
        text += f'{sv}\n'
        text += f'Открыто {data["sv_data"][sv]["open_shop"]} из {data["sv_data"][sv]["all_shop_count"]}\n'
        text += f'Ротации {data["sv_data"][sv]["rotate_shop"]} из {data["sv_data"][sv]["all_shop_count"]}\n'
        text += '\n'

    return {'main_message_text': text}


async def structure_changes(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.main_message.structure_changes>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    return {}


async def who_will_inspected(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.main_message.who_will_inspected>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_supervisors()

    return {
        'supervisors': data
    }
