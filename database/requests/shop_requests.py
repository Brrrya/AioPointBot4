from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.connect import session_maker
from database.models import Registers, Sellers, Shops, Supervisors, Directors


class ShopRequests:
    @staticmethod
    async def take_info_about_shop(shop_tgid: int):
        """Достает основную инфу по магазину из базы данных"""
        async with session_maker() as session:
            shop = await session.execute(
                select(Shops)
                .where(Shops.tgid == shop_tgid)
                .options(
                    selectinload(Shops.sv),
                    selectinload(Shops.seller)
                )
            )
            shop = shop.scalar()
            worker = shop.seller
            supervisor = shop.sv
            res = {
                'title': shop.title,
                'worker': f"✅ {worker.first_name} {worker.last_name}" if worker else "❌ Отсутствует",
                'worker_tgid': shop.worker,
                'supervisor': f"{supervisor.first_name} {supervisor.last_name}",
                'supervisor_tgid': shop.supervisor,
                'open_or_not': '❌ Закрыт' if shop.state is False else '✅ Открыт',
                'rotate_or_not': '❌ Не сделаны' if shop.rotate is False else '✅ Сделаны',
                'fridges_or_not': '⭕️ Выключены' if shop.fridges_state is False else '⚡️ Включены'
            }
        return res

    @staticmethod
    async def worker_authorization_on_shop(worker_badge: int, shop_tgid: int):
        """Функция авторизации, удаляет пользователя с авторизации другого магазина, если есть
        и авторизует его в текущем (ФУНКЦИЮ НАПИСАЛ СРАЗУ С ПЕРВОГО РАЗА!!!!)"""

        async with session_maker() as session:
            worker = await session.execute(select(Sellers).where(Sellers.badge == worker_badge))
            worker = worker.scalar()
            if worker:
                other_shop = await session.execute(select(Shops).where(Shops.worker == int(worker.tgid)))
                other_shop = other_shop.scalar()
                other_shop_tgid = None
                if other_shop:
                    other_shop_tgid = other_shop.tgid
                    other_shop.worker = None
                shop = await session.get(Shops, shop_tgid)
                shop.worker = worker.tgid
                result = {
                    'full_name': f'{worker.first_name} {worker.last_name}',
                    'tgid': worker.tgid,
                    'badge': worker.badge,
                    'other_shop_tgid': other_shop_tgid
                }
                await session.commit()
            else:
                return None
        return result

    @staticmethod
    async def badge_check(worker_badge: int):
        """Проверяет есть ли переданный бейдж в БД, если нет то возвращает True иначе False"""
        async with session_maker() as session:
            seller = await session.execute(select(Sellers).where(Sellers.badge == worker_badge))
            supervisor = await session.execute(select(Supervisors).where(Supervisors.badge == worker_badge))
            director = await session.execute(select(Directors).where(Directors.badge == worker_badge))
            register = await session.execute(select(Registers).where(Registers.badge == worker_badge))
            if seller.scalar() or supervisor.scalar() or director.scalar() or register.scalar():
                return False
        return True

    @staticmethod
    async def take_all_supervisors():
        """Возвращает список кортежей всех управляющих"""
        async with session_maker() as session:
            data = await session.execute(
                select(Supervisors)
                .order_by(Supervisors.last_name)
            )
            data = data.scalars().all()
            res = [
                (f'{i.last_name} {i.first_name}', i.tgid)
                for i in data
            ]
        return res


    @staticmethod
    async def insert_new_reg_user_in_db(
            first_name: str,
            last_name: str,
            supervisor_tgid: int,
            badge: int,
            reg_code: int
    ):
        """Вставляет нового пользователя в БД в регистрацию."""
        async with session_maker() as session:
            session.add(Registers(
                first_name=first_name,
                last_name=last_name,
                supervisor=supervisor_tgid,
                badge=badge,
                reg_code=reg_code
            ))
            await session.commit()


# async def main():
#     await ShopRequests.update_month_plan(5809674485)
#
# if __name__ == '__main__':
#     asyncio.run(main())