from datetime import date
from typing import Dict

from aiogram import F
from aiogram.types import CallbackQuery
from babel.dates import get_day_names, get_month_names

from aiogram_dialog import (
    Dialog, Window, DialogManager, ChatEvent,
)
from aiogram_dialog.widgets.kbd import (
    Calendar, CalendarScope, ManagedCalendar, SwitchTo,
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView, CalendarMonthView, CalendarScopeView, CalendarYearsView,
    DATE_TEXT, TODAY_TEXT, CalendarConfig, CalendarUserConfig,
)
from aiogram_dialog.widgets.text import Const, Text, Format
from dialogs.shop_dialogs.plan_change_dialog import states

SELECTED_DAYS_KEY = "selected_dates"


class CustomCalendarDaysView(CalendarDaysView):
    async def render(
            self,
            config: CalendarUserConfig,
            offset: date,
            data: Dict,
            manager: DialogManager,
    ):
        return [
            # await self._render_header(config, offset, data, manager),
            await self._render_week_header(config, data, manager),
            *await self._render_days(config, offset, data, manager),
            # await self._render_pager(config, offset, data, manager),
        ]


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_day_names(
            width="short", context='stand-alone', locale=locale,
        )[selected_date.weekday()].title()


class MarkedDay(Text):
    def __init__(self, mark: str, other: Text):
        super().__init__()
        self.mark = mark
        self.other = other

    async def _render_text(self, data, manager: DialogManager) -> str:
        current_date: date = data["date"]
        serial_date = current_date.isoformat()
        selected = manager.dialog_data.get(SELECTED_DAYS_KEY, [])
        if serial_date in selected:
            return self.mark
        return await self.other.render_text(data, manager)


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            'wide', context='stand-alone', locale=locale,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CustomCalendarDaysView(
                self._item_callback_data,
                weekday_text=WeekDay(),
                config=CalendarConfig()
            ),
        }


async def on_date_clicked(
        callback: ChatEvent, widget: ManagedCalendar,
        manager: DialogManager,
        selected_date: date, /
):
    await callback.answer(str(selected_date))


async def on_date_selected(
        callback: ChatEvent, widget: ManagedCalendar,
        manager: DialogManager,
        clicked_date: date, /
):
    selected = manager.dialog_data.setdefault(SELECTED_DAYS_KEY, [])
    serial_date = clicked_date.isoformat()
    if serial_date in selected:
        selected.remove(serial_date)
    else:
        selected.append(serial_date)


async def selection_getter(dialog_manager, **_):
    selected = dialog_manager.dialog_data.get(SELECTED_DAYS_KEY, [])
    return {
        "selected": ", ".join(sorted(selected))
    }


