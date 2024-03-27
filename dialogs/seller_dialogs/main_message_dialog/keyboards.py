from aiogram import F
from aiogram_dialog.widgets.kbd import Group, Button, Row, StubScroll, NumberedPager, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format


def main_message_kb(open_shop, close_shop, rotate_shop, on_fridges, off_fridges):
    return Group(
        Row(
            Button(Const('🔑 Открыть'), on_click=open_shop, id='open_shop'),
            Button(Const('📱 Ротации'), on_click=rotate_shop, id='rotate_shop'),
            ),
        Row(
            Button(Const('📱 Вкл. холодильник'), on_click=on_fridges, id='on_fridges_shop'),
            Button(Const('🔑 Выкл. холодильник'), on_click=off_fridges, id='off_fridges_shop'),
        ),
        Row(
            Button(Const('🔒 Закрыть'), on_click=close_shop, id='close_shop'),
        ),

        id='seller_main_message_group',
    )


def take_photos_on_fridges_shop(on_delete, send_report, go_back):
    return Group(
        Button(Const('✉️ Отправить фото холодильников'), id='send_fridges_to_sv',
               on_click=send_report, when='media_count'),
        StubScroll(id="pages", pages="media_count"),
        Group(
            NumberedPager(scroll="pages", when=F["pages"] > 1),
            width=4
        ),
        Button(Format("🗑️ Удалить фото #{media_number}"), id="del",
               on_click=on_delete, when="media_count"),
        Row(
            Button(Const('⬅️ Назад'), on_click=go_back, id="go_back_fridges"),
        ),

    )
