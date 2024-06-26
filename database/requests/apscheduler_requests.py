import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.connect import session_maker
from database.models import *


class APScgedulerRequests:
    @staticmethod
    async def not_open_shop_warning():
        """Собирает список неоткрытых магазинов для управляющего и проверяющего"""
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
                    & (Shops.state == False)
                )
                .order_by(Shops.title)
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
        """Собирает список не закрытых магазинов для управляющего"""
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
        """Собирает список тех, кто ещё не сделал ротации для управляющего и проверяюшего"""
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
                    & (Shops.rotate == False)
                )
                .order_by(Shops.title)
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
    async def reset_all_everyday():
        """Обнуляет все магазины и все регистрации, и возвращает списки всех сотрудников и магазинов"""
        async with session_maker() as session:
            shops = await session.execute(
                select(Shops)
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()
            res_shop = []
            for shop in shops:
                shop.state = False
                shop.rotate = False
                shop.worker = None
                res_shop.append(shop.tgid)

            reg_users = await session.execute(
                select(Registers)
            )
            reg_users = reg_users.scalars().all()

            if reg_users:
                for user in reg_users:
                    await session.delete(user)


            sellers = await session.execute(
                select(Sellers)
                .where(Sellers.badge != None)
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
        """Возвращает название и тг айди всех магазинов"""
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


    @staticmethod
    async def turn_fridges(action: bool):
        """action True - Вкл ХО, action False - Выкл ХО"""
        """Собирает список тех, кто ещё не Вкл/Выкл ХО для управляющего и проверяюшего"""
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
                    if action is True:
                        if shop.fridges_state is True:
                            sv_res.append(shop.title)
                    else:
                        if shop.fridges_state is False:
                            sv_res.append(shop.title)

                res_for_sv[sv.tgid] = (
                    (shop_name,) for shop_name in sv_res
                )

            if action is True:
                all_shop = await session.execute(
                    select(Shops)
                    .where(
                        (Shops.fridges_checker != None)
                        & (Shops.fridges_state == True)
                    )
                    .order_by(Shops.title)
                )
            else:
                all_shop = await session.execute(
                    select(Shops)
                    .where(
                        (Shops.fridges_checker != None)
                        & (Shops.fridges_state == False)
                    )
                    .order_by(Shops.title)
                )
            all_shop = all_shop.scalars().all()

            res_for_checker = {}
            for shop in all_shop:
                keys = res_for_checker.keys()
                if shop.fridges_checker in keys:
                    res_for_checker[shop.fridges_checker].append(shop.title)
                else:
                    res_for_checker[shop.fridges_checker] = [shop.title]

            res = {
                'sv': res_for_sv,
                'checker': res_for_checker
            }
            return res



if __name__ == '__main__':
    asyncio.run(APScgedulerRequests.not_open_shop_warning())
