import asyncio
import calendar
import datetime
from datetime import datetime

import ezodf

from database.requests.plan_requests import PlanRequests


async def update_coefficients(
        monday: int = 20,
        tuesday: int = 25,
        wednesday: int = 25,
        thursday: int = 28,
        friday: int = 30,
        saturday: int = 35,
        sunday: int = 25
):
    """Обновляем коэффициенты под каждый месяц, так как разная их длина епта"""

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
    await PlanRequests.recreate_coefs(coefficients, c_full)

async def create_plan(
        point_tgid: int
):

    data = await PlanRequests.take_plan_data(point_tgid)
    # point_data: list[str | int] = await db.database.select_all_data_about_tt(point_tgid)
    # plan_data = await db.database.select_all_plan_data(point_data[1])

    doc = ezodf.newdoc(doctype='ods', filename=f'service/plans/{data["shop_data"]["shop_title"]}.ods')
    sheets = doc.sheets
    sheets += ezodf.Table("Sheet1", size=(40, 15))
    sheet = sheets[0]

    sheet["A1"].set_value("Дата")
    sheet["B1"].set_value("План РТО")
    sheet["C1"].set_value("Факт РТО")
    sheet["D1"].set_value("План ЦКП")
    sheet["E1"].set_value("Факт ЦКП")
    sheet["F1"].set_value("План чеков")
    sheet["G1"].set_value("Факт чеков")
    sheet["H1"].set_value("Факт дисконт карт")

    checks_all = 0
    RTO_all = 0
    CKP_all = 0
    count = 2

    sum_plan_rto = None
    sum_plan_ckp = None
    sum_plan_check = None

    for p_data in data['shop_plan']:

        if sum_plan_check is None:
            sum_plan_rto = p_data[8]
            sum_plan_ckp = p_data[9]
            sum_plan_check = p_data[10]

        sheet[f"A{count}"].set_value(p_data[0])
        sheet[f"B{count}"].set_value(p_data[1])
        try:
            sheet[f"C{count}"].set_value(p_data[2])
        except:
            sheet[f"C{count}"].set_value(0)
        sheet[f"D{count}"].set_value(p_data[3])
        try:
            sheet[f"E{count}"].set_value(p_data[4])
        except:
            sheet[f"E{count}"].set_value(0)
        sheet[f"F{count}"].set_value(p_data[5])
        try:
            sheet[f"G{count}"].set_value(p_data[6])
        except:
            sheet[f"G{count}"].set_value(0)
        try:
            sheet[f"H{count}"].set_value(p_data[7])
        except:
            sheet[f"H{count}"].set_value(0)

        count += 1
        RTO_all += p_data[2] if p_data[2] is not None else 0
        CKP_all += p_data[4] if p_data[4] is not None else 0
        checks_all += p_data[6] if p_data[6] is not None else 0

    sheet["K5"].set_value("Общий план РТО")
    sheet["J5"].set_value(sum_plan_rto)
    sheet["K6"].set_value("Общий факт РТО")
    sheet["J6"].set_value(RTO_all)
    sheet["K7"].set_value("Процент выполнения")
    try:
        sheet["J7"].set_value(100 * (RTO_all / sum_plan_rto))
    except:
        sheet["J7"].set_value(0)

    sheet["K9"].set_value("Общий план чеков")
    sheet["J9"].set_value(sum_plan_check)
    sheet["K10"].set_value("Общий факт чеков")
    sheet["J10"].set_value(checks_all)
    sheet["K11"].set_value("Процент выполнения")
    try:
        sheet["J11"].set_value(100 * (checks_all / sum_plan_check))
    except:
        sheet["J11"].set_value(0)

    sheet["K13"].set_value("Общий план ЦКП")
    sheet["J13"].set_value(sum_plan_ckp)
    sheet["K14"].set_value("Общий факт ЦКП")
    sheet["J14"].set_value(CKP_all)
    sheet["K15"].set_value("Процент выполнения")
    try:
        sheet["J15"].set_value(100 * (CKP_all / sum_plan_ckp))
    except:
        sheet["J15"].set_value(0)

    doc.save()



if __name__ == '__main__':
    asyncio.run(create_plan(5809674485))

