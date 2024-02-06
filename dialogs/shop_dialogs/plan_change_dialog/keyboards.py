from custom_items.customcalendar import CustomCalendar


def calendar_for_change_plan(on_click):
    cal = CustomCalendar(
        id='calendar_for_change_plan_',
        on_click=on_click
    )
    return cal
