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

            return res


    @staticmethod
    async def select_all_workers():
        """Возвращает список всех продавцов"""
        async with session_maker() as session:
            sellers = await session.execute(
                select(Sellers)
                .order_by(Sellers.last_name)
            )
            sellers = sellers.scalars().all()

            res = [
                (f'{seller.last_name} {seller.first_name}', seller.tgid)
                for seller in sellers
            ]

            return res


    @staticmethod
    async def select_data_about_seller(seller_tgid: int):
        """Возвращает информацию о сотруднике"""
        async with session_maker() as session:
            seller = await session.get(
                Sellers, seller_tgid
            )

            res = {
                'full_name': f'{seller.last_name} {seller.first_name}',
                'tgid': seller.tgid,
                'sv': seller.supervisor,
                'badge': seller.badge
            }

            return res


    @staticmethod
    async def appoint_supervisor(new_sv_tgid: int):
        """Добавляет сотрудника к СВ убирает из продавцов"""
        async with session_maker() as session:
            seller = await session.get(
                Sellers, new_sv_tgid
            )

            shop_with_seller = await session.execute(
                select(Shops)
                .where(
                    (Shops.worker == seller.tgid)
                    | (Shops.open_checker == seller.tgid)
                    | (Shops.rotate_checker == seller.tgid))
            )
            shop_with_seller = shop_with_seller.scalars().all()


            res = {
                'was_authorized': False
            }
            if shop_with_seller:
                """Если авторизирован или проверяющий в магазине убираем от туда"""
                for shop in shop_with_seller:
                    if shop.worker == seller.tgid:
                        shop.worker = None
                        res['was_authorized'] = True
                        res.update(where_was_authorized_tgid=shop.tgid)

                    if shop.open_checker == seller.tgid:
                        shop.open_checker = None

                    if shop.rotate_checker == seller.tgid:
                        shop.rotate_checker = None

                await session.flush()

            session.add(Supervisors(
                first_name=seller.first_name, last_name=seller.last_name,
                tgid=seller.tgid, badge=seller.badge)
            )

            await session.delete(seller)

            await session.commit()

        # async with session_maker() as session:
        #     seller = session.get(Sellers, new_sv_tgid)
        #     session.delete(seller)
        #     await session.commit()
        #
        return res

if __name__ == '__main__':
    asyncio.run(DirectorRequests.main_message_info())

