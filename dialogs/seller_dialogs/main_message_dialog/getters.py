from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from database.seller_requests import SellerRequests


async def main_message(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.event.from_user.id
    return await SellerRequests.take_main_window_info(user)


async def open_photo_confirm(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    image = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(ctx.dialog_data.get('open_photo')))
    return {
        'photo': image
    }


async def rotate_photo_confirm(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    image = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(ctx.dialog_data.get('rotate_photo')))
    return {
        'photo': image
    }

