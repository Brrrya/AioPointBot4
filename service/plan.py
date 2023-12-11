import asyncio
import calendar
from datetime import datetime
import datetime
import ezodf

from database.unknown_requests import UnknownRequests


async def update_coefficients(
        monday: int = 20,
        tuesday: int = 25,
        wednesday: int = 25,
        thursday: int = 28,
        friday: int = 30,
        saturday: int = 35,
        sunday: int = 25
):
    # Обновляем коэффициенты под каждый месяц, так как разная их длина епта

    # Получаем текущую дату и определяем количество дней в месяце
    now = datetime.datetime.now()
    how_many_days_in_month = calendar.monthrange(now.year, now.month)[1]

    # Создаем список coefficients с нулевыми значениями
    coefficients = [0] * how_many_days_in_month

    # Определяем коэффициент для каждого дня недели текущего месяца
    for day in range(1, how_many_days_in_month+1):
        date = datetime.date(now.year, now.month, day)
        day_of_week = date.weekday()
        if day_of_week == 0:
            coefficients[day-1] = monday
        elif day_of_week == 1:
            coefficients[day-1] = tuesday
        elif day_of_week == 2:
            coefficients[day-1] = wednesday
        elif day_of_week == 3:
            coefficients[day-1] = thursday
        elif day_of_week == 4:
            coefficients[day-1] = friday
        elif day_of_week == 5:
            coefficients[day-1] = saturday
        elif day_of_week == 6:
            coefficients[day-1] = sunday

    c_full = sum(coefficients)  # переменная для общего коэфа

    # Закидываем данные в функцию, которая записывает всё в БД
    await UnknownRequests.recreate_coefs(coefficients, c_full)






if __name__ == '__main__':
    asyncio.run(update_coefficients())

