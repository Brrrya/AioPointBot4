import asyncio
import logging

from logging.handlers import RotatingFileHandler
from logging import Formatter

# from loguru import logger

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder


from aiogram.types import BotCommand

from aiogram_dialog import setup_dialogs

from config.config import load_config
from commands import register_user_commands
from commands.bot_commands import all_commands

from dialogs import register_all_dialogs

from service import scheduler

async def main() -> None:
    # root_logger = logging.getLogger('root_loger')
    # root_logger.setLevel(logging.DEBUG)
    log_handler = RotatingFileHandler(filename='../logs/log.log', maxBytes=128000000, backupCount=5)
    log_handler.setFormatter(Formatter("%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"))

    logging.basicConfig(level=logging.DEBUG, filemode='a',
                        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", )
    logging.getLogger('').addHandler(log_handler)

    # logger.add('../logs/log.log', format='{time} {level} {message}', level='DEBUG', rotation='00:30',
    #            compression='zip')


    commands_for_bot = []
    for command in all_commands:
        commands_for_bot.append(BotCommand(command=command[0], description=command[1]))

    config = load_config()

    storage = RedisStorage.from_url(url=config.redis_db.db_url, key_builder=DefaultKeyBuilder(with_destiny=True))

    dp = Dispatcher(events_isolation=SimpleEventIsolation(), storage=storage)
    bot = Bot(config.tgbot.token)

    await bot.set_my_commands(commands_for_bot)
    register_user_commands(dp)
    await register_all_dialogs(dp)
    setups = setup_dialogs(dp)

    await scheduler.create_tasks(bot, setups)

    await bot.delete_webhook(drop_pending_updates=True)  # Пропускаем апдейты
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot was stopped")
