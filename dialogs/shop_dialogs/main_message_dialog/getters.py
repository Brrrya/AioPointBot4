import logging

from aiogram_dialog import DialogManager

from database.requests.shop_requests import ShopRequests


async def main_message(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Shop.main_message.main_message>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    user = dialog_manager.event.from_user.id
    shop = await ShopRequests.take_info_about_shop(user)
    return shop


async def authorization(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Shop.main_message.authorization>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}
