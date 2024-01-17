import calendar
from datetime import date, datetime, timedelta

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarConfig


def calendar_for_change_plan(on_click):
    cal = Calendar(
        id='calendar_for_change_plan_',
        config=CalendarConfig(
            min_date=date(date.today().year, date.today().month, 1),
            max_date=date(date.today().year, date.today().month,
                          calendar.monthrange(date.today().year, date.today().month)[1]),
        ),
        on_click=on_click
    )
    return cal
