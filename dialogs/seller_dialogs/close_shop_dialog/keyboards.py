from aiogram import F

from aiogram_dialog.widgets.kbd import Back, Cancel, Group, Button, Row, StubScroll, NumberedPager
from aiogram_dialog.widgets.text import Const, Format


def take_photos_close_shop(on_delete, send_report):
    return Group(
        Button(Const('✉️ Отправить отчет управляющему'), id='send_message_to_sv',
               on_click=send_report, when='media_count'),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=4
        ),
        Button(Format("🗑️ Удалить фото #{media_number}"), id="del",
               on_click=on_delete, when="media_count"),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад')),
        ),

    )


