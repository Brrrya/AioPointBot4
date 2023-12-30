import logging

from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from aiogram_dialog import DialogManager

from database.requests.seller_requests import SellerRequests


async def plug(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.Plug>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}


async def main_message(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.MainWindow>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()

    user = dialog_manager.event.from_user.id
    data = await SellerRequests.take_main_window_info(user)
    ctx.dialog_data.update(shop_tgid=data['shop_tgid'])
    return data


async def open_photo_take(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.open_photo_take>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}


async def open_photo_confirm(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.open_photo_confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    image = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(ctx.dialog_data.get('open_photo')))
    return {
        'photo': image
    }


async def rotate_photo_take(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.rotate_photo_take>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}


async def rotate_photo_confirm(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.rotate_photo_confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    image = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(ctx.dialog_data.get('rotate_photo')))
    return {
        'photo': image
    }

