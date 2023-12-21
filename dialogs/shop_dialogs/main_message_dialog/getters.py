from aiogram_dialog import DialogManager

from database.requests.shop_requests import ShopRequests


async def main_message(dialog_manager: DialogManager, **kwargs):
    user = dialog_manager.event.from_user.id
    shop = await ShopRequests.take_info_about_shop(user)
    # await dialog_manager.bg(shop['supervisor_tgid'], shop['supervisor_tgid']).update(data=dialog_manager.start_data)
    return shop
