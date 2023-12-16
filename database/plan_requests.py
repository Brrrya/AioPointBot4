import asyncio
import calendar
import datetime

from sqlalchemy import update, select, insert, text, MetaData, Table, Column, Integer, String, Date, delete
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import selectinload


from database.connect import session_maker
from database.models import *


class PlanRequests:
    @staticmethod
    async def take_plan_data(
            shop_tgid: int
    ):
        async with session_maker() as session:
            shop = await session.get(Shops, shop_tgid)

            try:
                # Проверяем обновлен ли план у магазина
                shop_plan = await session.execute(
                    text(
                        f"SELECT "
                        f"(date_, plan_rto, fact_rto, plan_ckp, fact_ckp, plan_check, fact_check,"
                        f"fact_dcart, sum_plan_rto, sum_plan_ckp, sum_plan_check) "
                        f"FROM {shop.bd_title} ORDER BY date_ ASC"
                    )
                )
                shop_plan = shop_plan.scalars().all()
                res = {
                    'shop_data': {
                        'shop_title': shop.title
                    },
                    'shop_plan': (
                        (plan[0], plan[1], plan[2], plan[3], plan[4],
                         plan[5], plan[6], plan[7],
                         plan[8], plan[9], plan[10])
                        for plan in shop_plan
                    )
                }
                return res
            except:
                # Если нет, то завершаем сессию и будет выполнен код, что внизу функции
                await session.rollback()

        # Если у магазина не создан план, то выполниться эта часть кода и создаст план со стандартными знач.
        await PlanRequests.update_plan(1000000, 100000, 1000, shop_tgid)
        # А затем вернет эту же функцию, что по итогу всё же выполнит её
        return await PlanRequests.take_plan_data(shop_tgid)

    @staticmethod
    async def update_plan(
            rto: int,
            ckp: int,
            check: int,
            shop_tgid: int
    ):
        async with session_maker() as session:
            shop = await session.get(Shops, shop_tgid)

            metadata = MetaData()
            tables = Table(
                shop.bd_title,
                metadata,
                Column('id', Integer, primary_key=True),
                Column('date_', Date, nullable=False),
                Column('plan_rto', Integer, nullable=False),
                Column('fact_rto', Integer, nullable=True),
                Column('plan_ckp', Integer, nullable=False),
                Column('fact_ckp', Integer, nullable=True),
                Column('plan_check', Integer, nullable=False),
                Column('fact_check', Integer, nullable=True),
                Column('fact_dcart', Integer, nullable=True),
                Column('sum_plan_rto', Integer, nullable=False),
                Column('sum_plan_ckp', Integer, nullable=False),
                Column('sum_plan_check', Integer, nullable=False),
            )
            await session.execute(CreateTable(tables, if_not_exists=True))

            # Проверяем есть ли в таблице какие-либо данные.
            row_count = await session.execute(
                text(f'SELECT COUNT(*) FROM {shop.bd_title}')
            )
            row_count = row_count.scalar()

            # Генерируем данные для текущего месяца
            current_date = datetime.datetime.now().date()
            current_month = current_date.month
            days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
            coefficients = await session.execute(select(Coefs))
            coefficients = coefficients.scalars().all()
            coefficient_full = coefficients[0].full_coef

            some_row = await session.execute(
                text(f'SELECT date_ FROM {shop.bd_title}')
            )
            some_row = some_row.scalar()


            if some_row is not None and some_row.month != current_month:
                # Если прошлого месяца, надо отправить таблицу пользователю, а затем очистить
                await session.execute(
                    text(f'TRUNCATE {shop.bd_title} RESTART IDENTITY')
                )

            for i in range(days_in_month):
                # вычесляет выручку на каждый день
                a = coefficients[i].coef
                pc = int(rto) / coefficient_full * a
                pc = int(pc)

                pckp = int(ckp) / coefficient_full * a
                pckp = int(pckp)

                # вычесляет колво чеков на каждый день
                pch = int(check) / coefficient_full * a
                pch = int(pch)
                if row_count == 0 or (row_count != 0 and some_row is not None and some_row.month != current_month):
                    await session.execute(
                        insert(tables)
                        .values(date_=datetime.date(current_date.year, current_month, i + 1),
                                          plan_rto=pc, plan_ckp=pckp, plan_check=pch,
                                          sum_plan_rto=rto, sum_plan_ckp=ckp, sum_plan_check=check)
                    )
                else:
                    await session.execute(
                        update(tables)
                        .values(date_=datetime.date(current_date.year, current_month, i + 1),
                                plan_rto=pc, plan_ckp=pckp, plan_check=pch,
                                sum_plan_rto=rto, sum_plan_ckp=ckp, sum_plan_check=check)
                        .where(tables.columns.date_ == datetime.date(current_date.year, current_month, i + 1))
                    )

            await session.commit()


    @staticmethod
    async def recreate_coefs(
            coefficients: list[int],
            full_coeff: int
    ):
        async with session_maker() as session:
            await session.execute(
                delete(Coefs)
            )
            await session.flush()

            for coef in coefficients:
                await session.execute(
                    insert(Coefs)
                    .values(coef=coef, full_coef=full_coeff)
                )

            await session.commit()




if __name__ == '__main__':
    asyncio.run(PlanRequests.recreate_coefs(coefficients=[30,35,25,20,25,25,28,30,35,25,20,25,25,28,30,35,25,20,25,25,28,30,35,25,20,25,25,28,30,35,25],
                                            full_coeff=842))

#     asyncio.run(PlanRequests.update_plan(
#         shop_tgid=5809674485,
#         rto=2000000,
#         ckp=200000,
#         check=1500,
#         ))
