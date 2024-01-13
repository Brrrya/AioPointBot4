import logging
from dataclasses import dataclass

from environs import Env

from config.telegram import TgBot
from config.database import Database
from config.redis import Redis_DB


@dataclass
class Config:
    tgbot: TgBot
    database: Database
    redis_db: Redis_DB

def load_config() -> Config:
    """Create configurate datatype"""

    env: Env = Env()   # Создаем экземпляр класса Env
    env.read_env('.env')   # Добавляем в переменные окружения данные, прочитанные из файла .env

    logging.info('Конфиг загружен')

    return Config(tgbot=TgBot(token=env('BOT_TOKEN')),
                  database=Database(
                      db_name=env('DB_NAME'),
                      db_user=env('DB_USER'),
                      db_password=env('DB_PASSWORD'),
                      db_url=env('DB_URL'),
                      db_port=env('DB_PORT')
                  ),
                  redis_db=Redis_DB(
                      db_host=env('REDIS_HOST'),
                      db_password=env('REDIS_PASSWORD'),
                      db_port=env('REDIS_PORT'),
                      db_num=env('REDIS_DB'),
                      db_url=f'redis://:{env("REDIS_PASSWORD")}@{env("REDIS_HOST")}:{env("REDIS_PORT")}/{env("REDIS_DB")}')
                  )





