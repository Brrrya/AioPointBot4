import asyncio
import datetime

from sqlalchemy import select, MetaData, Table, Column, Integer, String, Date
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import selectinload


from database.connect import session_maker
from database.models import *

class APScgedulerRequests:
    @staticmethod
    async def not_open_shop_warning():
        async with session_maker() as session:
            sv_all = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops))
            )
            sv_all = sv_all.scalars().all()

            res_for_sv = {}
            for sv in sv_all:
                sv_res = []
                for shop in sv.shops:
                    if shop.state is False:
                        sv_res.append(shop.title)
                res_for_sv[sv.tgid] = (
                    (shop_name,) for shop_name in sv_res
                )

            all_shop = await session.execute(
                select(Shops)
                .where(
                    (Shops.open_checker != None)
                    &(Shops.state == False)
                )
            )
            all_shop = all_shop.scalars().all()
            res_for_checker = {}
            for shop in all_shop:
                keys = res_for_checker.keys()
                if shop.open_checker in keys:
                    res_for_checker[shop.open_checker].append(shop.title)
                else:
                    res_for_checker[shop.open_checker] = [shop.title]

            res = {
                'sv': res_for_sv,
                'checker': res_for_checker
            }
            return res
    @staticmethod
    async def who_not_close_shops():
        async with session_maker() as session:
            all_sv = await session.execute(
                select(Supervisors)
                .options(
                    selectinload(Supervisors.shops)
                )
            )
            all_sv = all_sv.scalars().all()

            res = {}
            for sv in all_sv:
                sv_res = []
                for shop in sv.shops:
                    if shop.state is True:
                        sv_res.append(shop.title)
                res[sv.tgid] = (
                    (shop_name,) for shop_name in sv_res
                )
            return res


    @staticmethod
    async def who_not_make_rotate():
        async with session_maker() as session:
            sv_all = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops))
            )
            sv_all = sv_all.scalars().all()

            res_for_sv = {}
            for sv in sv_all:
                sv_res = []
                for shop in sv.shops:
                    if shop.rotate is False:
                        sv_res.append(shop.title)
                res_for_sv[sv.tgid] = (
                    (shop_name,) for shop_name in sv_res
                )

            all_shop = await session.execute(
                select(Shops)
                .where(
                    (Shops.rotate_checker != None)
                    &(Shops.rotate == False)
                )
            )
            all_shop = all_shop.scalars().all()

            res_for_checker = {}
            for shop in all_shop:
                keys = res_for_checker.keys()
                if shop.rotate_checker in keys:
                    res_for_checker[shop.rotate_checker].append(shop.title)
                else:
                    res_for_checker[shop.rotate_checker] = [shop.title]

            res = {
                'sv': res_for_sv,
                'checker': res_for_checker
            }
            return res


    @staticmethod
    async def reset_all_shops():
        async with session_maker() as session:
            shops = await session.execute(
                select(Shops)
            )
            shops = shops.scalars().all()
            res_shop = []
            for shop in shops:
                shop.state = False
                shop.rotate = False
                shop.worker = None
                res_shop.append(shop.tgid)


            sellers = await session.execute(
                select(Sellers)
            )
            sellers = sellers.scalars().all()
            res_seller = []
            for seller in sellers:
                res_seller.append(seller.tgid)

            supervisors = await session.execute(
                select(Supervisors)
            )
            supervisors = supervisors.scalars().all()
            res_supervisor = []
            for supervisor in supervisors:
                res_supervisor.append(supervisor.tgid)

            res = {
                'shops': res_shop,
                'sellers': res_seller,
                'supervisors': res_supervisor,
            }
            await session.commit()
        return res


    @staticmethod
    async def take_all_shop():
        async with session_maker() as session:
            all_shops = await session.execute(
                select(Shops)
            )
            all_shops = all_shops.scalars().all()

            res = {
                'all_shops': (
                    (shop.title, shop.tgid,) for shop in all_shops
                )
            }
        return res

if __name__ == '__main__':
    asyncio.run(APScgedulerRequests.not_open_shop_warning())
