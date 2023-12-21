from aiogram import Dispatcher

from dialogs import (
    shop_dialogs, seller_dialogs, supervisor_dialogs, director_dialogs
)


async def register_all_dialogs(dp: Dispatcher):
    """Регистрирует все диалоги"""
    for dialog in [
        *await shop_dialogs.all_shop_dialogs(),
        *await seller_dialogs.all_shop_dialogs(),
        *await supervisor_dialogs.all_supervisor_dialogs(),
        # *await director_dialogs.all_director_dialogs(),
    ]:
        dp.include_router(dialog)
