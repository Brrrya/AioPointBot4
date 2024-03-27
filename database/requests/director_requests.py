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
                .where(Sellers.badge != None)
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
                sv_fridges_on_count = 0
                sv_shop_count = 0

                for shop in sv.shops:

                    if shop.state is True:
                        sv_open_shop_count += 1
                    if shop.rotate is True:
                        sv_rotate_shop_count += 1
                    if shop.fridges_state is True:
                        sv_fridges_on_count += 1

                    sv_shop_count += 1

                res['sv_data'][f'{sv.last_name} {sv.first_name}']=\
                    {
                        'all_shop_count': sv_shop_count,
                        'open_shop': sv_open_shop_count,
                        'rotate_shop': sv_rotate_shop_count,
                        'fridges_on': sv_fridges_on_count
                    }

        return res


    @staticmethod
    async def select_all_shops():
        """Возвращает список всех магазинов"""
        async with session_maker() as session:
            shops = await session.execute(
                select(Shops)
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()

            res = [
                (shop.title, shop.tgid)
                for shop in shops
            ]

        return res

    @staticmethod
    async def select_all_workers():
        """Возвращает список всех продавцов"""
        async with session_maker() as session:
            sellers = await session.execute(
                select(Sellers)
                .order_by(Sellers.last_name)
                .where(Sellers.badge != None)
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
        """Добавляет сотрудника к СВ убирает из продавцов и проверяющих"""
        async with session_maker() as session:
            seller = await session.get(
                Sellers, new_sv_tgid
            )

            shop_with_seller = await session.execute(
                select(Shops)
                .where(
                    (Shops.worker == seller.tgid)
                    | (Shops.open_checker == seller.tgid)
                    | (Shops.rotate_checker == seller.tgid)
                    | (Shops.close_checker == seller.tgid))
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

                    if shop.close_checker == seller.tgid:
                        shop.close_checker = None

                await session.flush()

            session.add(Supervisors(
                first_name=seller.first_name, last_name=seller.last_name,
                tgid=seller.tgid, badge=seller.badge)
            )

            await session.delete(seller)

            await session.commit()

        return res


    @staticmethod
    async def select_all_supervisors():
        """Возвращает список всех СВ"""
        async with session_maker() as session:
            sv = await session.execute(
                select(Supervisors)
                .order_by(Supervisors.last_name)
            )
            sv = sv.scalars().all()

            res = [
                (f'{supervisor.last_name} {supervisor.first_name}', supervisor.tgid)
                for supervisor in sv
            ]

        return res


    @staticmethod
    async def select_data_about_fire_sv(sv_tgid: int):
        """Возвращает информацию об увольняймом св"""
        async with session_maker() as session:
            data = await session.execute(
                select(Supervisors)
                .where(Supervisors.tgid == sv_tgid)
                .options(selectinload(Supervisors.sellers))
                .options(selectinload(Supervisors.shops))
            )

            sv = data.scalar()



            shops_count = 0
            sellers_count = 0
            some_thing = True

            if sv.shops:
                some_thing = False
                for shop in sv.shops:
                    shops_count += 1

            if sv.sellers:
                some_thing = False
                for seller in sv.sellers:
                    sellers_count += 1

        return {
            'some_thing': some_thing,
            'shops_count': shops_count,
            'seller_count': sellers_count,
            'sv_name': f'{sv.last_name} {sv.first_name}'
        }


    @staticmethod
    async def fire_sv(sv_tgid: int):
        """Удаляет супервайзера из базы данных"""
        async with session_maker() as session:
            sv = await session.get(Supervisors, sv_tgid)

            reg_users = await session.execute(
                select(Registers)
                .where(Registers.supervisor == sv_tgid)
            )
            reg_users = reg_users.scalars().all()

            if reg_users:
                for user in reg_users:
                    await session.delete(user)

            await session.delete(sv)
            await session.commit()

    @staticmethod
    async def fire_seller(seller_tgid):
        """Удаляет продавца из бд и убирает его с проверяющих"""
        async with session_maker() as session:
            seller = await session.get(Sellers, seller_tgid)

            shop_with_seller = await session.execute(
                select(Shops)
                .where(
                    (Shops.worker == seller.tgid)
                    | (Shops.open_checker == seller.tgid)
                    | (Shops.rotate_checker == seller.tgid)
                    | (Shops.close_checker == seller.tgid))
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

                    if shop.close_checker == seller.tgid:
                        shop.close_checker = None

                await session.flush()

            # await session.delete(seller)
            seller.badge = None
            seller.supervisor = None
            await session.commit()

        return res


    @staticmethod
    async def take_data_for_transfer_seller(
            old_sv_tgid: int | None,
            new_sv_tgid: int,
            seller_tgid: int | None,
            all_or_not: bool

    ):
        """Возвращает данные для подтверждения передачи сотрудника"""
        async with session_maker() as session:
            new_sv = await session.get(Supervisors, new_sv_tgid)
            if all_or_not is True:
                seller = await session.get(Sellers, seller_tgid)
                old_sv = await session.get(Supervisors, seller.supervisor)
            else:
                old_sv = await session.get(Supervisors, old_sv_tgid)

        return {
            'old_sv_data': {
                'full_name': f'{old_sv.last_name} {old_sv.first_name}'
            },
            'new_sv_data': {
                'full_name': f'{new_sv.last_name} {new_sv.first_name}'
            },
            'seller_data': {
                'full_name': f'{seller.last_name} {seller.first_name}' if all_or_not is True else None
            }
        }


    @staticmethod
    async def transfer_sellers(
            old_sv_tgid: int | None,
            new_sv_tgid: int,
            seller_tgid: int | None,
            all_or_not: bool
    ):
        async with session_maker() as session:
            if all_or_not is True:
                old_sv = await session.execute(
                    select(Supervisors)
                    .where(Supervisors.tgid == old_sv_tgid)
                    .options(
                        selectinload(Supervisors.sellers)
                    )
                )
                old_sv = old_sv.scalar()

                for seller in old_sv.sellers:
                    seller.supervisor = new_sv_tgid

            else:
                seller = await session.get(Sellers, seller_tgid)
                seller.supervisor = new_sv_tgid

            await session.commit()


    @staticmethod
    async def take_data_for_transfer_shop(
            old_sv_tgid: int | None,
            new_sv_tgid: int,
            shop_tgid: int | None,
            all_or_not: bool

    ):
        """Возвращает данные для подтверждения передачи магазина"""
        async with session_maker() as session:
            new_sv = await session.get(Supervisors, new_sv_tgid)
            if all_or_not is True:
                shop = await session.get(Shops, shop_tgid)
                old_sv = await session.get(Supervisors, shop.supervisor)
            else:
                old_sv = await session.get(Supervisors, old_sv_tgid)

        return {
            'old_sv_data': {
                'full_name': f'{old_sv.last_name} {old_sv.first_name}'
            },
            'new_sv_data': {
                'full_name': f'{new_sv.last_name} {new_sv.first_name}'
            },
            'shop_data': {
                'full_name': shop.title if all_or_not is True else None
            }
        }

    @staticmethod
    async def transfer_shops(
            old_sv_tgid: int | None,
            new_sv_tgid: int,
            shop_tgid: int | None,
            all_or_not: bool
    ):
        async with session_maker() as session:
            if all_or_not is True:
                old_sv = await session.execute(
                    select(Supervisors)
                    .where(Supervisors.tgid == old_sv_tgid)
                    .options(
                        selectinload(Supervisors.shops)
                    )
                )
                old_sv = old_sv.scalar()

                for shop in old_sv.shops:
                    shop.supervisor = new_sv_tgid

            else:
                shop = await session.get(Shops, shop_tgid)
                shop.supervisor = new_sv_tgid

            await session.commit()





if __name__ == '__main__':
    asyncio.run(DirectorRequests.select_data_about_fire_sv(109338928))

