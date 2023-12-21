import logging

from aiogram.types import Message

from commands.bot_commands import all_commands


async def help_command(message: Message) -> None:
    """Выводит список команд бота"""
    logging.info(f'Ввел команду /help id={message.from_user.id} username={message.from_user.username}')
    text_answer = 'Список всех команд бота:\n\n'
    for command in all_commands:
        text_answer += f'{command[0]} - {command[2]} \n'

    await message.answer(text=text_answer)

