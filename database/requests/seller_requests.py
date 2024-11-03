import datetime

from sqlalchemy import select

from database.connect import session_maker
from database.models import Sellers, Shops, Supervisors, Photos, Reports


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
                'rotate_or_not': '❌ Не сделаны' if data.rotate is False else '✅ Сделаны',
                'fridges_or_not': '⭕️ Выключены' if data.fridges_state is False else '⚡️ Включены'
            }

        return res


    @staticmethod
    async def insert_photo(seller_tgid: int, action: str, photos_tgid: list[str]):
        """Вставляет фото в БД с текущей датой
        Из действий open, rotate, close, fridges_on, fridges_off"""
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
            elif action == 'fridges_on':
                shop.fridges_state = True
            elif action == 'fridges_off':
                shop.fridges_state = False
            await session.commit()

    @staticmethod
    async def save_report(
            rto: int | None,
            check: int | None,
            p_rto: int | None,
            p_check: int | None,
            shop_tgid: int,
            seller_tgid: int,
            ckp: int | None = None,
            p_ckp: int | None = None,
            dcart: int | None = None,
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
                p_rto=p_rto,
                p_ckp=p_ckp,
                p_check=p_check
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
                    if photo:
                        all_photos.append((photo.photo_tgid, shop.title))
                    else:
                        who_not_do.append((shop.title, shop.tgid))

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
                    if photo:
                        all_photos.append((photo.photo_tgid, shop.title))
                    else:
                        who_not_do.append((shop.title, shop.tgid))

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
    async def checker_reports(
            checker_tgid: int
    ):
        """Возвращает отчеты магазинов, за которым закреплен проверяющим"""
        async with session_maker() as session:
            # Получаем список магазинов СВ
            shops = await session.execute(
                select(Shops)
                .where(
                    (Shops.close_checker == checker_tgid)
                )
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()

            result = {}
            counter = 0
            for shop in shops:
                # Проходимся по всем магазинам и собираем вечерний отчет каждого
                report = await session.execute(
                    select(Reports)
                    .where(
                        (Reports.report_date == datetime.date.today())
                        & (Reports.shop_tgid == shop.tgid)
                    )
                )
                report = report.scalar()
                if report:
                    # Если есть вечерний отчет
                    photo_list = []
                    photos = await session.execute(  # Получаем фото вечернего отчета
                        select(Photos)
                        .where(
                            (Photos.shop_tgid == shop.tgid)
                            & (Photos.action == 'close')
                            & (Photos.p_date == datetime.date.today())
                        )
                    )
                    photos = photos.scalars().all()

                    for photo in photos:
                        photo_list.append(photo.photo_tgid)  # Добавляем эти фото в список

                    report_seller = await session.get(Sellers,
                                                      report.seller_tgid)  # Находим сотрудника который закрывался
                    result.update(
                        {
                            counter: {
                                'shop_name': shop.title,
                                'seller_name': f'{report_seller.last_name} {report_seller.first_name}',
                                'rto': report.rto,
                                'ckp': report.ckp,
                                'check': report.check,
                                'dcart': report.dcart,
                                'p_rto': report.p_rto,
                                'p_ckp': report.p_ckp,
                                'p_check': report.p_check,
                                'photos': photo_list,
                            }
                        }
                    )
                    counter += 1
        return result

    @staticmethod
    async def checker_report_who_not_send(
            checker_tgid: int
    ):
        """Возвращает тех, кто ещё не скинул отчет закрытия за ткущий день"""
        async with session_maker() as session:
            shops = await session.execute(
                select(Shops)
                .where(Shops.close_checker == checker_tgid)
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()

            close_report_or_not = True
            without_report = []
            for shop in shops:
                report = await session.execute(
                    select(Reports)
                    .where(
                        (Reports.report_date == datetime.date.today())
                        & (Reports.shop_tgid == shop.tgid)
                    )
                )
                report = report.scalar()
                if report is None:
                    close_report_or_not = False
                    without_report.append(shop.title)

            res = {
                'all_not_close_report': (
                    (shop_name,) for shop_name in without_report  # Список ещё не отправивших отчёт закрытия
                ),
                'close_report_or_not': close_report_or_not  #  Если все отправили отчёт закрытия то True
            }
        return res

    @staticmethod
    async def checker_all_photo_on_fridges(checker_id: int, photos_action: bool, photos_date: datetime.date | None = None):
        """
        :param checker_id:
        :param photos_action: True == fridges_on, False == fridges_off
        :param photos_date:
        :return:
        """
        if photos_date is None:
            photos_date = datetime.datetime.today().date()
        """Возвращает фото холодильников"""
        async with session_maker() as session:
            # Получаем список магазинов где назначен проверяющим ХО
            shops = await session.execute(
                select(Shops)
                .where(
                    (Shops.fridges_checker == checker_id)
                )
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()

            photos_actions_text = 'fridges_on' if photos_action is True else 'fridges_off'

            result = {}
            who_not_do = []
            counter = 0
            for shop in shops:
                if shop.fridges_state is photos_action:

                    photos = await session.execute(  # Получаем фото холодильников
                        select(Photos)
                        .where(
                            (Photos.shop_tgid == shop.tgid)
                            & (Photos.action == photos_actions_text)
                            & (
                                (Photos.p_date == photos_date)
                                |
                                (Photos.p_date == (photos_date - datetime.timedelta(days=1)))

                            )
                        )
                    )
                    photos = photos.scalars().all()

                    photo_list_previous_day = []
                    photo_list_current_day = []

                    if photos:
                        for photo in photos:
                            if photo.p_date == photos_date:
                                photo_list_current_day.append(photo.photo_tgid)  # Добавляем эти фото в список
                            else:
                                photo_list_previous_day.append(photo.photo_tgid)

                    result.update(
                        {
                            counter: {
                                'shop_name': shop.title,
                                'photos': photo_list_current_day if photo_list_current_day else photo_list_previous_day,
                            }
                        }
                    )
                    counter += 1

                else:
                    who_not_do.append(shop.title)
        full_res = {
            'reports': result,
            'who_not_send': who_not_do
        }
        return full_res



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
