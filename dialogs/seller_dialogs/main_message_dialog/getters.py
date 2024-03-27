import logging

from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll

from database.requests.seller_requests import SellerRequests

async def plug(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.Plug>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    return {}


async def register_command(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.register_command>'
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


async def take_photos_on(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.take_photos_on>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = dialog_manager.dialog_data.get("photos_on", [])
    if photos:
        photo = photos[media_number]
        media = MediaAttachment(
            file_id=MediaId(*photo),
            type=ContentType.PHOTO,
        )
    else:
        media = MediaAttachment(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637",
            type=ContentType.PHOTO,
        )

    return {
        "media_count": len(photos),
        "media_number": media_number + 1,
        "media": media,
    }



async def take_photos_off(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.main_dialog.take_photos_off>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = dialog_manager.dialog_data.get("photos_off", [])
    if photos:
        photo = photos[media_number]
        media = MediaAttachment(
            file_id=MediaId(*photo),
            type=ContentType.PHOTO,
        )
    else:
        media = MediaAttachment(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637",
            type=ContentType.PHOTO,
        )

    return {
        "media_count": len(photos),
        "media_number": media_number + 1,
        "media": media,
    }
