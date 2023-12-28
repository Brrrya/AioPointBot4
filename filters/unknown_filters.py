from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.requests.unknown_requests import UnknownRequests


class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message):
        who_cant_reg = await UnknownRequests.who_cant_register()

        if message.from_user.id in who_cant_reg:
            return False
        else:
            return True


