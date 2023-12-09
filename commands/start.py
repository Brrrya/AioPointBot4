from aiogram.types import Message

from aiogram_dialog import DialogManager

from dialogs.shop_dialogs.main_message_dialog.states import MainMessage as ShopMainMessage
from dialogs.seller_dialogs.main_message_dialog.states import MainMessageUser as UserMainMessage
from dialogs.supervisor_dialogs.main_message_dialog.states import MainMessageSupervisor as SupervisorMainMessage


from database.unknown_requests import UnknownRequests


async def start(message: Message, dialog_manager: DialogManager):
    res = await UnknownRequests.user_first_auth(message.from_user.id)
    if res == 'shop':
        await dialog_manager.start(ShopMainMessage.main_message)
    elif res == 'seller':
        auth_or_not = await UnknownRequests.user_check_auth(message.from_user.id)
        if auth_or_not is True:
            await dialog_manager.start(UserMainMessage.main_message)
        else:
            await dialog_manager.start(UserMainMessage.plug)
    elif res == 'supervisor':
        await dialog_manager.start(SupervisorMainMessage.main_message)
    else:
        await message.answer('Пук среньк')
