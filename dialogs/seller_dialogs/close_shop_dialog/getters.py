from aiogram.types import CallbackQuery
from aiogram.enums import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.common import ManagedScroll


from database.seller_requests import SellerRequests


async def close_take_ckp(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'close_rto': f"✅ {ctx.dialog_data.get('close_rto')}"
    }


async def close_take_check(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'close_rto': f"✅ {ctx.dialog_data.get('close_rto')}",
        'close_ckp': f"✅ {ctx.dialog_data.get('close_ckp')}",
    }


async def close_take_dcart(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'close_rto': f"✅ {ctx.dialog_data.get('close_rto')}",
        'close_ckp': f"✅ {ctx.dialog_data.get('close_ckp')}",
        'close_check': f"✅ {ctx.dialog_data.get('close_check')}",
    }


async def close_take_photos(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()

    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = dialog_manager.dialog_data.get("photos", [])
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
        'close_rto': f"✅ {ctx.dialog_data.get('close_rto')}",
        'close_ckp': f"✅ {ctx.dialog_data.get('close_ckp')}",
        'close_check': f"✅ {ctx.dialog_data.get('close_check')}",
        'close_dcart': f"✅ {ctx.dialog_data.get('close_dcart')}",
        "media_count": len(photos),
        "media_number": media_number + 1,
        "media": media,
    }

