from dataclasses import dataclass

from environs import Env

from config.telegram import TgBot
from config.database import Database


@dataclass
class Config:
    tgbot: TgBot
    database: Database


def load_config() -> Config:
    """Create configurate datatype"""

    env: Env = Env()   # Создаем экземпляр класса Env
    env.read_env('.env')   # Добавляем в переменные окружения данные, прочитанные из файла .env

    print("Config was loaded")

    return Config(tgbot=TgBot(token=env('BOT_TOKEN')),
                  database=Database(
                      db_name=env('DB_NAME'),
                      db_user=env('DB_USER'),
                      db_password=env('DB_PASSWORD'),
                      db_url=env('DB_URL')
                  ))





