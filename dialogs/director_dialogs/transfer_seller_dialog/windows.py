from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const, Case, Multi

from dialogs.director_dialogs.transfer_seller_dialog import (
    getters, keyboards, selected, states
)


async def select_seller_for_transfer():
    return Window(
        Const('Тут можно переместить сотрудника от одного управляющего к другому или сразу всех сотрудников СВ'),
        Const('Выберете сотрудника для перемещения'),
        keyboards.choice_seller(on_click=selected.transfer_seller),
        Button(Const("📝 Всех сотрудников супервайзера"), id='dr_transfer_all_workers_sv', on_click=selected.transfer_all_by_sv),
        Cancel(Const('❌ Отмена')),
        getter=getters.select_seller_for_transfer,
        state=states.TransferSellerDirector.select_seller
    )


async def select_all_seller_for_transfer_by_sv():
    return Window(
        Const('Сотрудников какого СВ переместить?'),
        keyboards.choice_sv(on_click=selected.select_all_seller_for_transfer_by_sv),
        Cancel(Const('❌ Отмена')),
        getter=getters.select_all_seller_for_transfer_by_sv,
        state=states.TransferSellerDirector.select_sellers_by_sv
    )


async def who_will_take_sellers():
    return Window(
        Const('Какому СВ передать сотрудников?'),
        keyboards.choice_sv(on_click=selected.who_will_take_sellers),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад'))
        ),
        getter=getters.who_will_take_sellers,
        state=states.TransferSellerDirector.select_recipient
    )


async def confirm_seller_transfer():
    return Window(
        Const('Вы действительно хотите переместить:'),
        Case(
            {
                True: Multi(
                    Const('- Всех сотрудников'),
                    Format('(управляющего {old_sv_name})')
                ),
                False: Multi(
                    Format('- Сотрудника {seller_name}'),
                    Format('(текущий управляющий {old_sv_name})')
                )
            },
            selector='all_or_not'
        ),
        Const('Новому управляющему'),
        Format('- {new_sv_name}?'),
        Button(Const('✅ Да'), id='dr_confirm_seller_transfer', on_click=selected.confirm),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад'))
        ),
        getter=getters.confirm_seller_transfer,
        state=states.TransferSellerDirector.confirm
    )
