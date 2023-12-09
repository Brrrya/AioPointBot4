from sqlalchemy import select

from database.connect import session_maker
from database.models import Registers, Sellers, Shops, Supervisors, Directors


class UnknownRequests:
    @staticmethod
    async def select_register_user_by_reg_code(register_code: int, user_tgid: int):
        """ This function checking reg code
            If reg code is True, function add new user from table registers in table sellers"""
        async with session_maker() as session:
            register_user = await session.execute(select(Registers)
                                                  .where(Registers.reg_code == register_code))
            user: Registers = register_user.scalar()
            if user:
                session.add(
                    Sellers(first_name=user.first_name, last_name=user.last_name,
                            tgid=user_tgid, supervisor=user.supervisor)
                )
                await session.delete(user)
                await session.commit()
                return True
        return False

    @staticmethod
    async def user_first_auth(user_id: int) -> str:
        """ This function takes the user ID and checks what position the writer holds. """

        async with session_maker() as session:
            if await session.get(Sellers, user_id):
                return 'seller'
            elif await session.get(Shops, user_id):
                return 'shop'
            elif await session.get(Supervisors, user_id):
                return 'supervisor'
            elif await session.get(Directors, user_id):
                return 'director'

    @staticmethod
    async def user_check_auth(seller_tgid: int):
        """Проверяет авторизирован ли продавец на каком либо магазине"""
        async with session_maker() as session:
            data = await session.execute(select(Shops).where(Shops.worker == seller_tgid))
            data = data.scalar()
            if data:
                return True
            return False

