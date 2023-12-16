import asyncio
import datetime

from sqlalchemy import select

from sqlalchemy.orm import selectinload


from database.connect import session_maker
from database.models import Registers, Sellers, Shops, Supervisors, Directors, Photos, Reports


class SellerRequests:
    @staticmethod
    async def take_main_window_info(worker_tgid: int):
        """Достает основную инфу по магазину из базы данных"""
        async with session_maker() as session:
            # data = await session.get(Shops, shop_tgid)
            data = await session.execute(select(Shops).where(Shops.worker == worker_tgid))
            data = data.scalar()
            worker = await session.get(Sellers, data.worker) if data.worker else None
            supervisor = await session.get(Supervisors, data.supervisor)
            res = {
                'title': data.title,
                'shop_tgid': data.tgid,
                'worker': f"✅ {worker.first_name} {worker.last_name}" if worker else "❌ Отсутствует",
                'supervisor': f"{supervisor.first_name} {supervisor.last_name}",
                'open_or_not': '❌ Закрыт' if data.state is False else '✅ Открыт',
                'rotate_or_not': '❌ Не сделаны' if data.rotate is False else '✅ Сделаны'
            }
            return res


    @staticmethod
    async def insert_photo(seller_tgid: int, action: str, photos_tgid: list[str]):
        """Вставляет фото в БД с текущей датой
        Из действий open, rotate, close"""
        async with session_maker() as session:
            photo_list = []
            shop = await session.execute(select(Shops).where(Shops.worker == seller_tgid))
            shop = shop.scalar()
            for photo_tgid in photos_tgid:
                photo_list.append(Photos(photo_tgid=photo_tgid, shop_tgid=shop.tgid, action=action,
                                         p_date=datetime.date.today()))
            session.add_all(photo_list)
            if action == 'open':
                shop.state = True
            elif action == 'rotate':
                shop.rotate = True
            elif action == 'close':
                shop.rotate = False
                shop.state = False
                shop.worker = None
            await session.commit()

    @staticmethod
    async def save_report(
            rto: int,
            ckp: int,
            check: int,
            dcart: int,
            shop_tgid: int,
            seller_tgid: int
    ):
        """Сохраняет вечерний отчет в БД"""
        async with session_maker() as session:
            session.add(Reports(
                report_date=datetime.date.today(),
                shop_tgid=shop_tgid,
                seller_tgid=seller_tgid,
                rto=rto,
                ckp=ckp,
                check=check,
                dcart=dcart,
            ))
            await session.commit()


    @staticmethod
    async def checker_all_photo_open(
            checker_tgid: int,
    ):
        """Для проверяющих достаёт все фотки чеков открытия с их магазина"""
        async with session_maker() as session:
            shops = await session.execute(
                select(Shops)
                .where(
                    (Shops.open_checker == checker_tgid)
                )
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()

            all_make_action = True
            all_photos = []
            who_not_do = []
            for shop in shops:
                if shop.state is False:
                    all_make_action = False
                    who_not_do.append((shop.title, shop.tgid))
                else:
                    photo = await session.execute(
                        select(Photos).
                        where(
                            (Photos.shop_tgid == shop.tgid)
                            & (Photos.p_date == datetime.date.today())
                            & (Photos.action == 'open')
                        ),
                    )
                    photo = photo.scalar()
                    all_photos.append((photo.photo_tgid, shop.title))

            res = {
                'all_photo': (
                    (ph[0], ph[1]) for ph in all_photos
                ),
                'all_make_action': all_make_action,
                'who_not_do': (
                    (i[0], i[1]) for i in who_not_do
                )
            }
            return res


    @staticmethod
    async def checker_all_photo_rotate(
            checker_tgid: int,
    ):
        """Для проверяющих достаёт все фотки ротаций с их магазина"""
        async with session_maker() as session:
            shops = await session.execute(
                select(Shops)
                .where(Shops.rotate_checker == checker_tgid)
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()

            all_make_action = True
            all_photos = []
            who_not_do = []
            for shop in shops:
                if shop.rotate is False:
                    all_make_action = False
                    who_not_do.append((shop.title, shop.tgid))
                else:
                    photo = await session.execute(
                        select(Photos).
                        where(
                            (Photos.shop_tgid == shop.tgid)
                            & (Photos.p_date == datetime.date.today())
                            & (Photos.action == 'rotate')
                        ),
                    )
                    photo = photo.scalar()
                    all_photos.append((photo.photo_tgid, shop.title))

            res = {
                'all_photo': (
                    (ph[0], ph[1]) for ph in all_photos
                ),
                'all_make_action': all_make_action,
                'who_not_do': (
                    (i[0], i[1]) for i in who_not_do
                )
            }
            return res






# async def test():
#     res = await SellerRequests.checker_all_photo_open(799609102)
#     print('all_photo')
#     for photo in res['all_photo']:
#         print(photo[0], photo[1])
#     print(res['all_make_action'])
#     print('who_not_do')
#     for who in res['who_not_do']:
#         print(who[0], who[1])
#
# if __name__ == '__main__':
#     asyncio.run(test())
