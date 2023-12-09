from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from database.supervisor_requests import SupervisorRequests


async def who_will_deleted(dialog_manager: DialogManager, **kwargs):
    return await SupervisorRequests.take_all_sellers(dialog_manager.event.from_user.id)


async def confirm(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    data = await SupervisorRequests.take_data_about_seller_by_tgid(ctx.dialog_data.get('fire_seller_tgid'))
    return data
