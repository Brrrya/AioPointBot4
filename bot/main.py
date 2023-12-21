import asyncio
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.fsm.storage.redis import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs

from commands import register_user_commands
from commands.bot_commands import all_commands
from config.config import load_config
from dialogs import register_all_dialogs
from service import scheduler


async def main() -> None:
    # Создаем файлы логов и запускает логирование
    log_handler = RotatingFileHandler(filename='../logs/log.log', maxBytes=128000000, backupCount=5)
    log_handler.setFormatter(Formatter("%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"))

    logging.basicConfig(level=logging.DEBUG, filemode='a',
                        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", )
    logging.getLogger('').addHandler(log_handler)

    # Создает список команд для вывода в подсказках
    commands_for_bot = []
    for command in all_commands:
        commands_for_bot.append(BotCommand(command=command[0], description=command[1]))

    # Подгружает конфиг
    config = load_config()

    # Подключаем редис для хранения данных бота
    storage = RedisStorage.from_url(url=config.redis_db.db_url, key_builder=DefaultKeyBuilder(with_destiny=True))

    # Создаем диспетчер бота и объект самого бота
    dp = Dispatcher(events_isolation=SimpleEventIsolation(), storage=storage)
    bot = Bot(config.tgbot.token)

    # Устанавливаем подсказки команд и регистрируем хендлеры под них
    await bot.set_my_commands(commands_for_bot)
    register_user_commands(dp)

    # Регистрируем все диалоги бота
    await register_all_dialogs(dp)
    setups = setup_dialogs(dp)

    # Создаем таски завязанные по времени
    await scheduler.create_tasks(bot, setups)

    await bot.delete_webhook(drop_pending_updates=True)  # Пропускаем апдейты
    await dp.start_polling(bot)  # Запускам пуллинг бота

