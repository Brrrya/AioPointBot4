import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config.config import load_config


def link_create(db_name, db_user, db_pass, db_host, db_port) -> str:
    db_link = f'postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    return db_link


config = load_config()

engine = create_async_engine(
    link_create(
        config.database.db_name,
        config.database.db_user,
        config.database.db_password,
        config.database.db_url,
        config.database.db_port
    ),
    echo=False
)

logging.info('Engine was created')

session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
logging.info('Session was created')


class Base(DeclarativeBase):
    pass


logging.info('Base class was created')

