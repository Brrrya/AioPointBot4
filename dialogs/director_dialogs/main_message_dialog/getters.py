import asyncio

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests


async def main_message(dialog_manager: DialogManager, **kwargs):
    data = await DirectorRequests.main_message_info()

    text = 'Общие данные\n' \
           f'Всего СВ - {data["sv_count"]}\n' \
           f'Всего продавцов - {data["seller_count"]}\n\n'


    for sv in data['sv_data']:
        text += f'СВ - {sv}\n'
        text += f'Открыто {data["sv_data"][sv]["open_shop"]} из {data["sv_data"][sv]["all_shop_count"]}\n'
        text += f'Ротации {data["sv_data"][sv]["rotate_shop"]} из {data["sv_data"][sv]["all_shop_count"]}\n'
        text += '\n'

    return {'main_message_text': text}

