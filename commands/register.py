from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.states import UnknownFSM

from database.unknown_requests import UnknownRequests

async def register_command(message: Message, state: FSMContext) -> None:
    await message.answer("Введите код регистрации")
    await state.set_state(UnknownFSM.wait_reg_code)


async def register_command_check_reg_code(message: Message, state: FSMContext) -> None:
    try:
        if await UnknownRequests.select_register_user_by_reg_code(int(message.text), int(message.from_user.id)):
            await message.answer("Вы успешно зарегистрировались!")
        else:
            await message.answer("Регистрационный код не найден")
    except ValueError:
        await message.answer("Неверный формат регистрационного кода")

    await state.clear()


async def my_state(message: Message, state: FSMContext) -> None:
    print(await state.get_state())
    await message.answer('Test answer')
