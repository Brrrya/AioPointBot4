from aiogram.enums import ContentType
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Back, StubScroll, Group
from aiogram_dialog.widgets.input import MessageInput

from aiogram_dialog.widgets.kbd import Cancel

from dialogs.seller_dialogs.close_shop_dialog import (
    getters, keyboards, selected, states
)


async def close_take_rto():
    return Window(
        Const('Выручка РТО - ❌'),
        Const('Выручка ЦКП - ❌'),
        Const('Количество чеков - ❌'),
        Const('Создано дисконт. карт - ❌'),
        Const(' '),
        Const('Введите выручку РТО'),
        Cancel(Const('❌ Отмена')),
        MessageInput(selected.close_take_rto),
        state=states.MainMessageUserClose.close_take_rto
    )


async def close_take_ckp():
    return Window(
        Format('Выручка РТО - {close_rto}'),
        Const('Выручка ЦКП - ❌'),
        Const('Количество чеков - ❌'),
        Const('Создано дисконт. карт - ❌'),
        Const(' '),
        Const('Введите выручку ЦКП'),
        Back(Const('⬅️ Назад')),
        Cancel(Const('❌ Отмена')),
        MessageInput(selected.close_take_ckp),
        getter=getters.close_take_ckp,
        state=states.MainMessageUserClose.close_take_ckp
    )


async def close_take_check():
    return Window(
        Format('Выручка РТО - {close_rto}'),
        Format('Выручка ЦКП - {close_ckp}'),
        Const('Количество чеков - ❌'),
        Const('Создано дисконт. карт - ❌'),
        Const(' '),
        Const('Введите количество чеков за сегодня'),
        Back(Const('⬅️ Назад')),
        Cancel(Const('❌ Отмена')),
        MessageInput(selected.close_take_check),
        getter=getters.close_take_check,
        state=states.MainMessageUserClose.close_take_check
    )


async def close_take_dcart():
    return Window(
        Format('Выручка РТО - {close_rto}'),
        Format('Выручка ЦКП - {close_ckp}'),
        Format('Количество чеков - {close_check}'),
        Const('Создано дисконт. карт - ❌'),
        Const(' '),
        Const('Введите количество созданных дисконтных карт за сегодня'),
        Back(Const('⬅️ Назад')),
        Cancel(Const('️❌ Отмена')),
        MessageInput(selected.close_take_dcart),
        getter=getters.close_take_dcart,
        state=states.MainMessageUserClose.close_take_dcart
    )


async def close_take_photos():
    return Window(
        Format('Выручка РТО - {close_rto}'),
        Format('Выручка ЦКП - {close_ckp}'),
        Format('Количество чеков - {close_check}'),
        Format('Создано дисконт. карт - {close_dcart}'),
        Const(' '),
        Const('Отправьте фотографии чека закрытия, запечатанного инкассационного пакета '
              'и фотографию лампочки сигнализации или закрытой двери'),
        DynamicMedia(selector="media"),

        keyboards.take_photos_close_shop(on_delete=selected.on_delete_close_photo,
                                         send_report=selected.send_report_close_photo,
                                         ),

        MessageInput(content_types=[ContentType.PHOTO], func=selected.on_input_photo),


        getter=getters.close_take_photos,
        state=states.MainMessageUserClose.close_take_photos
    )

