import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.connect import session_maker
from database.models import Sellers, Shops, Supervisors, Photos, Reports


class SupervisorRequests:
    @staticmethod
    async def get_main_window_info(sv_tgid: int):
        """Достает основную инфу по всем магазинам супервизора"""
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
        """Возвращает список всех фотографий ротаций или чеков открытия определенного управляющего"""
        async with session_maker() as session:
            supervisor = await session.execute(
                select(Supervisors)
                .options(selectinload(Supervisors.shops))
                .where(Supervisors.tgid == sv_tgid)
            )

            supervisor = supervisor.scalar()
            res = []
            for shop in supervisor.shops:
                if (shop.rotate if action == 'rotate' else shop.state) is True:
                    photo = await session.execute(
                        select(Photos)
                        .where(
                            (Photos.shop_tgid == shop.tgid)
                            & (Photos.p_date == datetime.date.today())
                            & (Photos.action == action)
                        )
                    )
                    photo = photo.scalar()
                    if photo:
                        res.append((photo.photo_tgid, shop.title))

            return res

    @staticmethod
    async def take_all_open_shops(sv_tgid: int):
        """Возвращает список не открытых магазинов определенного управляющего"""
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
        """Возвращает список не сделавших ротации магазинов определенного управляющего"""
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
        """Возвращает список всех продавцов определенного управляющего"""
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
        """Возвращает список всех управляющих"""
        async with session_maker() as session:
            supervisors = await session.execute(
                select(Supervisors)
                .order_by(Supervisors.last_name)
            )
            supervisors = supervisors.scalars().all()
            return {
                'supervisors': (
                    (f'{supervisor.last_name} {supervisor.first_name}', supervisor.tgid) for supervisor in supervisors
                )
            }
    @staticmethod
    async def take_data_for_seller_transfer(sv_tgid: int, seller_tgid: int | None):
        """Возвращает информацию о выбранных управляющем и продавце"""
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
        """Перемещает сотрудника или всех сотрудников к другому управляющему"""
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
        """Возвращает список всех магазинов определенного управляющего"""
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
        """Перемещает магазин или все магазины к другому управляющему"""
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
        """Возвращает информацию о выбранном магазине и управляющем"""
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
        """Возвращает информацию о сотруднике по тг айди"""
        async with session_maker() as session:
            seller = await session.execute(
                select(Sellers)
                .where(Sellers.tgid == seller_tgid)
            )
            seller = seller.scalar()
            return {
                'full_name': f"{seller.last_name} {seller.first_name}",
                'tgid': seller.tgid,
                'sv': seller.supervisor
            }

    @staticmethod
    async def delete_seller(seller_tgid: int):
        """Удаляет сотрудника из БД"""
        async with session_maker() as session:
            shop_with_seller = await session.execute(
                select(Shops)
                .where(
                    (Shops.worker == seller_tgid)
                    | (Shops.open_checker == seller_tgid)
                    | (Shops.rotate_checker == seller_tgid)
                    | (Shops.close_checker == seller_tgid))
            )
            shop_with_seller = shop_with_seller.scalars().all()

            update_message = False
            shop_with_seller_tgid = None
            if shop_with_seller:
                for shop in shop_with_seller:
                    if shop.worker == seller_tgid:
                        shop.worker = None
                        update_message = True
                        shop_with_seller_tgid = shop.tgid

                    if shop.open_checker == seller_tgid:
                        shop.open_checker = None

                    if shop.rotate_checker == seller_tgid:
                        shop.rotate_checker = None

                    if shop.close_checker == seller_tgid:
                        shop.close_checker = None

            seller = await session.get(Sellers, seller_tgid)
            await session.delete(seller)
            await session.commit()

        return {
            'update_message': update_message,
            'shop_with_seller_tgid': shop_with_seller_tgid
        }


    @staticmethod
    async def take_checkers_data(sv_tgid: int):
        """Возвращает список проверяющих магазинов определнного управляющего"""
        async with session_maker() as session:
            shops = await session.execute(
                select(Shops)
                .where(Shops.supervisor == sv_tgid)
            )
            shops = shops.scalars().all()

            some_shops = False
            checker_data = []
            for shop in shops:
                some_shops = True

                if shop.open_checker:
                    open_checker = await session.get(Sellers, shop.open_checker)
                    open_checker_name = f'{open_checker.last_name} {open_checker.first_name}'
                else:
                    open_checker_name = 'отсутствует'

                if shop.rotate_checker:
                    rotate_checker = await session.get(Sellers, shop.rotate_checker)
                    rotate_checker_name = f'{rotate_checker.last_name} {rotate_checker.first_name}'
                else:
                    rotate_checker_name = 'отсутствует'

                checker_data.append((shop.title,
                                     open_checker_name,
                                     rotate_checker_name))

            res = {
                'some_shops': some_shops,
                'checkers': (
                    (checker[0], checker[1], checker[2]) for checker in checker_data
                )
            }
            return res


    @staticmethod
    async def take_shop_name(shop_tgid: int):
        """Возвращает название магазина"""
        async with session_maker() as session:
            shop = await session.get(Shops, shop_tgid)

            return {
                'shop_title': shop.title
            }

    @staticmethod
    async def update_checker(
            role: str,
            shop_tgid: int,
            seller_tgid: int | None,
    ):
        """Меняет проверяющего у магазина"""
        async with session_maker() as session:
            shop = await session.get(Shops, shop_tgid)

            if role == 'open':
                shop.open_checker = seller_tgid
            elif role == 'rotate':
                shop.rotate_checker = seller_tgid
            elif role == 'close':
                shop.close_checker = seller_tgid

            await session.commit()

    @staticmethod
    async def take_all_close_report_data(sv_tgid: int, report_date: datetime.date | None = None):
        if report_date is None:
            report_date = datetime.datetime.today().date()
        """Возвращает вечерние отчеты тех кто их отправил"""
        async with session_maker() as session:
            # Получаем список магазинов СВ
            shops = await session.execute(
                select(Shops)
                .where(
                    (Shops.supervisor == sv_tgid)
                )
                .order_by(Shops.title)
            )
            shops = shops.scalars().all()

            result = {}
            who_not_send_report = []
            counter = 0
            for shop in shops:
                # Проходимся по всем магазинам и собираем вечерний отчет каждого
                report = await session.execute(
                    select(Reports)
                    .where(
                        (Reports.report_date == report_date)
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
                            & (Photos.p_date == report_date)
                        )
                    )
                    photos = photos.scalars().all()

                    for photo in photos:
                        photo_list.append(photo.photo_tgid)  # Добавляем эти фото в список

                    report_seller = await session.get(Sellers, report.seller_tgid)  # Находим сотрудника который закрывался
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
                else:
                    who_not_send_report.append(shop.title)
        full_res = {
            'reports': result,
            'who_not_send': who_not_send_report
        }
        return full_res



# async def test():
#     res = await SupervisorRequests.take_all_close_report_data(5968177812)
#     keys = res.keys()
#     for key in keys:
#         print(res[key]['shop_name'])
#         print(res[key]['seller_name'])
#         print(res[key]['photos'])
#
# if __name__ == '__main__':
#     asyncio.run(test())
