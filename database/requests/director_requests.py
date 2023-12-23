import asyncio
import calendar
import datetime

from sqlalchemy import update, select, insert, text, MetaData, Table, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.schema import CreateTable

from database.connect import session_maker
from database.models import *


class DirectorRequests:
    @staticmethod
    async def main_message_info():
        async with session_maker() as session:
            sv_data = await session.execute(
                select(Supervisors)
                .options(
                    selectinload(Supervisors.shops),
                    selectinload(Supervisors.sellers)
                )
                .order_by(Supervisors.last_name)
            )
            sv_data = sv_data.scalars().all()

            sellers = await session.execute(
                select(Sellers)
                .order_by(Sellers.last_name)
            )
            sellers = sellers.scalars().all()

            res = {
                'sv_data': {},
                'sv_count': len(sv_data),
                'seller_count': len(sellers)
            }

            for sv in sv_data:
                sv_open_shop_count = 0
                sv_rotate_shop_count = 0
                sv_shop_count = 0

                for shop in sv.shops:

                    if shop.state is True:
                        sv_open_shop_count += 1
                    if shop.rotate is True:
                        sv_rotate_shop_count += 1

                    sv_shop_count += 1

                res['sv_data'][f'{sv.last_name} {sv.first_name}']=\
                    {
                        'all_shop_count': sv_shop_count,
                        'open_shop': sv_open_shop_count,
                        'rotate_shop': sv_rotate_shop_count
                    }

            print(res)
            return res








if __name__ == '__main__':
    asyncio.run(DirectorRequests.main_message_info())

