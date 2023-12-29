from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const, Case, Multi

from dialogs.director_dialogs.transfer_shop_dialog import (
    getters, keyboards, selected, states
)


async def select_shop_for_transfer():
    return Window(
        Const('Тут можно переместить магазин от одного управляющего к другому или сразу все магазины СВ'),
        Const('Выберете магазин для перемещения'),
        keyboards.choice_shop(on_click=selected.transfer_shop),
        Button(Const("📝 Все магазины супервайзера"), id='dr_transfer_all_shops_sv', on_click=selected.transfer_all_by_sv),
        Cancel(Const('❌ Отмена')),
        getter=getters.select_shops_for_transfer,
        state=states.TransferShopDirector.select_shop
    )


async def select_all_shops_for_transfer_by_sv():
    return Window(
        Const('Магазины какого СВ переместить?'),
        keyboards.choice_sv(on_click=selected.select_all_shops_for_transfer_by_sv),
        Cancel(Const('❌ Отмена')),
        getter=getters.select_all_shops_for_transfer_by_sv,
        state=states.TransferShopDirector.select_shops_by_sv
    )


async def who_will_take_shops():
    return Window(
        Const('Какому СВ передать магазины?'),
        keyboards.choice_sv(on_click=selected.who_will_take_shop),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад'))
        ),
        getter=getters.who_will_take_shops,
        state=states.TransferShopDirector.select_recipient
    )


async def confirm_shop_transfer():
    return Window(
        Const('Вы действительно хотите переместить:'),
        Case(
            {
                True: Multi(
                    Const('- Все магазины'),
                    Format('(управляющего {old_sv_name})')
                ),
                False: Multi(
                    Format('- Магазин {shop_name}'),
                    Format('(текущий управляющий {old_sv_name})')
                )
            },
            selector='all_or_not'
        ),
        Const('Новому управляющему'),
        Format('- {new_sv_name}?'),
        Button(Const('✅ Да'), id='dr_confirm_shop_transfer', on_click=selected.confirm),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад'))
        ),
        getter=getters.confirm_shop_transfer,
        state=states.TransferShopDirector.confirm
    )
