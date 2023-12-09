import asyncio
import datetime

from sqlalchemy import select, asc

from sqlalchemy.orm import selectinload

from database.connect import session_maker
from database.models import Registers, Sellers, Shops, Supervisors, Directors, Photos


class SupervisorRequests:
    @staticmethod
    async def get_main_window_info(sv_tgid: int):
        async with session_maker() as session:
            supervisor = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops).subqueryload(Shops.seller))
                .where(Supervisors.tgid == sv_tgid)
            )
            supervisor = supervisor.scalar()


            result: dict = {
                'shops_data': (
                    (shop.title,
                     '❌ отсутствует' if shop.worker is None else f'✅ {shop.seller.first_name} {shop.seller.last_name}',
                     "❌ закрыт" if shop.state is False else '✅ открыт',
                     "❌ не сделаны" if shop.rotate is False else '✅ сделаны')
                    for shop in supervisor.shops
                ),
                'no_shops': False if supervisor.shops else True
            }
        return result

    @staticmethod
    async def take_all_photo_rotate_or_state(sv_tgid: int, action: str):
        async with session_maker() as session:
            supervisor = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops))
                .where(Supervisors.tgid == sv_tgid)
            )
            supervisor = supervisor.scalar()
            res = []
            for shop in supervisor.shops:
                if shop.rotate if action == 'rotate' else shop.state is True:
                    photo = await session.execute(
                        select(Photos)
                        .where(
                            Photos.shop_tgid == shop.tgid
                            and Photos.p_date == datetime.date.today()
                            and Photos.action == action
                        )
                    )
                    photo = photo.scalar()
                    res.append((photo.photo_tgid, shop.title))
            return res

    @staticmethod
    async def take_all_open_shops(sv_tgid:int):
        async with session_maker() as session:
            supervisor = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops))
                .where(Supervisors.tgid == sv_tgid)
            )
            supervisor = supervisor.scalar()

            open_or_not = True
            close_shop = []
            for shop in supervisor.shops:
                if shop.state is False:
                    open_or_not = False
                    close_shop.append(shop.title)

            return{
                'all_not_open': (
                    (shop,) for shop in close_shop
                ),
                'open_or_not': open_or_not
            }

    @staticmethod
    async def take_all_rotate_shops(sv_tgid: int):
        async with session_maker() as session:
            supervisor = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops))
                .where(Supervisors.tgid == sv_tgid)
            )
            supervisor = supervisor.scalar()

            rotate_or_not = True
            not_rotate_shop = []
            for shop in supervisor.shops:
                if shop.rotate is False:
                    rotate_or_not = False
                    not_rotate_shop.append(shop.title)

            return{
                'all_not_rotate': (
                    (shop,) for shop in not_rotate_shop
                ),
                'rotate_or_not': rotate_or_not
            }

    @staticmethod
    async def take_all_sellers(sv_tgid: int):
        async with session_maker() as session:
            supervisor = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.sellers))
                .where(Supervisors.tgid == sv_tgid)
            )
            supervisor = supervisor.scalar()
        return {
            'sellers_list': (
                (f'{seller.last_name} {seller.first_name}', seller.tgid) for seller in supervisor.sellers
            ),
            'more_then_nobody': True if supervisor.sellers else False
        }

    @staticmethod
    async def take_all_sv():
        async with session_maker() as session:
            supervisors = await session.execute(
                select(Supervisors)
            )
            supervisors = supervisors.scalars().all()
            return {
                'supervisors': (
                    (f'{supervisor.last_name} {supervisor.first_name}', supervisor.tgid) for supervisor in supervisors
                )
            }
    @staticmethod
    async def take_data_for_seller_transfer(sv_tgid: int, seller_tgid: int | None):
        async with session_maker() as session:
            if seller_tgid:
                seller = await session.get(Sellers, seller_tgid)
            sv = await session.get(Supervisors, sv_tgid)

            return {
                'sv_name': f'{sv.last_name} {sv.first_name}',
                'seller_name': f'{seller.last_name} {seller.first_name}' if seller_tgid else None
            }


    @staticmethod
    async def seller_transfer(
            current_sv_tgid: int,
            new_sv_tgid: int,
            seller_tgid: int | None
    ):
        async with session_maker() as session:
            if seller_tgid:
                seller = await session.get(Sellers, seller_tgid)
                seller.supervisor = new_sv_tgid
            else:
                sellers_for_transfer = await session.execute(
                    select(Sellers)
                    .where(Sellers.supervisor == current_sv_tgid)
                )
                sellers_for_transfer = sellers_for_transfer.scalars().all()
                for seller in sellers_for_transfer:
                    seller.supervisor = new_sv_tgid
            await session.commit()


    @staticmethod
    async def take_all_shops(sv_tgid: int):
        async with session_maker() as session:
            supervisor = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops))
                .where(Supervisors.tgid == sv_tgid)
            )
            supervisor = supervisor.scalar()
        return {
            'shops_list': (
                (shop.title, shop.tgid) for shop in supervisor.shops
            ),
            'more_then_nobody': True if supervisor.shops else False
        }

    @staticmethod
    async def shop_transfer(
            current_sv_tgid: int,
            new_sv_tgid: int,
            shop_tgid: int | None
    ):
        async with session_maker() as session:
            if shop_tgid:
                shop = await session.get(Shops, shop_tgid)
                shop.supervisor = new_sv_tgid
            else:
                shops_for_transfer = await session.execute(
                    select(Shops)
                    .where(Shops.supervisor == current_sv_tgid)
                )
                shops_for_transfer = shops_for_transfer.scalars().all()
                for shop in shops_for_transfer:
                    shop.supervisor = new_sv_tgid
            await session.commit()


    @staticmethod
    async def take_data_for_shop_transfer(sv_tgid: int, shop_tgid: int | None):
        async with session_maker() as session:
            if shop_tgid:
                shop = await session.get(Shops, shop_tgid)
            sv = await session.get(Supervisors, sv_tgid)

            return {
                'sv_name': f'{sv.last_name} {sv.first_name}',
                'shop_title': shop.title if shop_tgid else None
            }

    @staticmethod
    async def take_data_about_seller_by_tgid(seller_tgid: int):
        async with session_maker() as session:
            seller = await session.execute(
                select(Sellers)
                .where(Sellers.tgid == seller_tgid)
            )
            seller = seller.scalar()
            return {
                'full_name': f"{seller.first_name} {seller.last_name}",
                'tgid': seller.tgid,
                'sv': seller.supervisor
            }

    @staticmethod
    async def delete_seller(seller_tgid: int):
        async with session_maker() as session:
            shop_with_seller = await session.execute(
                select(Shops)
                .where(Shops.worker == seller_tgid)
            )
            shop_with_seller = shop_with_seller.scalar()

            update_message = False
            shop_with_seller_tgid = None
            if shop_with_seller:
                shop_with_seller.worker = None
                update_message = True
                shop_with_seller_tgid = shop_with_seller.tgid

            seller = await session.get(Sellers, seller_tgid)
            await session.delete(seller)
            await session.commit()

        return {
            'update_message': update_message,
            'shop_with_seller_tgid': shop_with_seller_tgid
        }


if __name__ == '__main__':
    asyncio.run(SupervisorRequests.take_all_open_shops(5968177812))
