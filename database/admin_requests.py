import asyncio
import datetime

from sqlalchemy import select, MetaData, Table, Column, Integer, String, Date
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import selectinload


from database.connect import session_maker
from database.models import *


class AdminRequests:
    pass
    # @staticmethod
    # async def create_shop_plan_tables():
    #     # Функция должна запускаться при старте бота, чтобы единовременно создать
    #     # все необходимые таблицы под план для каждого магазина
    #     async with session_maker() as session:
    #         shops = await session.execute(
    #             select(Shops)
    #         )
    #         shops = shops.scalars().all()
    #         metadata = MetaData()
    #
    #         for shop in shops:
    #             tables = Table(
    #                 shop.bd_title,
    #                 metadata,
    #                 Column('id', Integer, primary_key=True),
    #                 Column('date_', Date, nullable=False),
    #                 Column('plan_rto', Integer, nullable=False),
    #                 Column('fact_rto', Integer, nullable=True),
    #                 Column('plan_ckp', Integer, nullable=False),
    #                 Column('fact_ckp', Integer, nullable=True),
    #                 Column('plan_check', Integer, nullable=False),
    #                 Column('fact_check', Integer, nullable=True),
    #                 Column('fact_dcart', Integer, nullable=True),
    #                 Column('sum_plan_rto', Integer, nullable=False),
    #                 Column('sum_plan_check', Integer, nullable=False),
    #                 Column('sum_plan_ckp', Integer, nullable=False)
    #             )
    #             await session.execute(CreateTable(tables, if_not_exists=True))
    #         await session.commit()


