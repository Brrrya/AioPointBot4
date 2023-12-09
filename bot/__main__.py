import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import BotCommand

from aiogram_dialog import setup_dialogs

from config.config import load_config
from commands import register_user_commands
from commands.bot_commands import all_commands

from dialogs import register_all_dialogs

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for command in all_commands:
        commands_for_bot.append(BotCommand(command=command[0], description=command[1]))

    config = load_config()

    dp = Dispatcher(events_isolation=SimpleEventIsolation())
    bot = Bot(config.tgbot.token)
    await bot.set_my_commands(commands_for_bot)


    register_user_commands(dp)
    await register_all_dialogs(dp)
    setup_dialogs(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot was stopped")
