import logging

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.states import UnknownFSM

from database.requests.unknown_requests import UnknownRequests

async def register_command(message: Message, state: FSMContext) -> None:
    """Срабатывает на команду /register"""
    logging.info(f'Ввел команду /register id={message.from_user.id} username={message.from_user.username}')
    await message.answer("Введите код регистрации")
    await state.set_state(UnknownFSM.wait_reg_code)


async def register_command_check_reg_code(message: Message, state: FSMContext) -> None:
    """Ловит введенный код регистрации после команды /register"""
    logging.info(f'Ввел код регистрации - {message.text} id={message.from_user.id} username={message.from_user.username}')
    try:
        if await UnknownRequests.select_register_user_by_reg_code(int(message.text), int(message.from_user.id)):
            logging.info(f'Успешно зарегистрирован id={message.from_user.id} username={message.from_user.username}')
            await message.answer("Вы успешно зарегистрировались!")
        else:
            logging.info(f'Неверный код регистрации id={message.from_user.id} username={message.from_user.username}')
            await message.answer("Регистрационный код не найден")
    except ValueError:
        logging.info(f'Неверный формат регистрационного кода id={message.from_user.id} username={message.from_user.username}')
        await message.answer("Неверный формат регистрационного кода")

    await state.clear()


async def my_state(message: Message, state: FSMContext) -> None:
    """Отладочная функция"""
    print(await state.get_state())
    await message.answer('Test answer')
