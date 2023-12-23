import logging

from aiogram.types import Message
from aiogram_dialog import DialogManager
from loguru import logger

from database.requests.unknown_requests import UnknownRequests
from dialogs.seller_dialogs.main_message_dialog.states import MainMessageUser as UserMainMessage
from dialogs.shop_dialogs.main_message_dialog.states import MainMessage as ShopMainMessage
from dialogs.supervisor_dialogs.main_message_dialog.states import MainMessageSupervisor as SupervisorMainMessage
from dialogs.director_dialogs.main_message_dialog.states import MainMessageDirector as DirectorMainMessage

# from dialogs.admin_dialogs.main_message_dialog.states import MainMessage as AdminMainMessage


async def start(message: Message, dialog_manager: DialogManager):
    """Определяет в какой диалог отправить пользователя"""
    logging.info(f'Ввел команду /start id={message.from_user.id} username={message.from_user.username}')
    res = await UnknownRequests.user_first_auth(message.from_user.id)
    if res == 'shop':
        await dialog_manager.start(ShopMainMessage.main_message)
    elif res == 'seller':
        # Проверяет если продавец авторизирован на магазине, выводит основное окно, иначе заглушку
        auth_or_not = await UnknownRequests.user_check_auth(message.from_user.id)
        if auth_or_not is True:
            await dialog_manager.start(UserMainMessage.main_message)
        else:
            await dialog_manager.start(UserMainMessage.plug)
    elif res == 'supervisor':
        await dialog_manager.start(SupervisorMainMessage.main_message)
    elif res == 'director':
        await dialog_manager.start(DirectorMainMessage.main_message)


    # elif res == 'admin':
        # await dialog_manager.start(AdminMainMessage.main_message)
    else:
        logger.info(f'Неизвестный пользователь id={message.from_user.id} username={message.from_user.username}')
        await message.answer('неизвестный пользователь')
