from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const, Case

from dialogs.supervisor_dialogs.seller_transfer_dialog import (
    getters, keyboards, selected, states
)


async def who_will_transfer():
    return Window(
        Case(
            {
                True:
                    Const("Какого сотрудника передать?"),
                False:
                    Const('За вами никто не закреплен')
            },
            selector='more_then_nobody'
        ),
        keyboards.all_sellers_by_sv(
            seller_choice=selected.seller_choice,
        ),
        Button(Const("📝 Всех"), id='all_seller_choice_for_transfer',
               when='more_then_nobody', on_click=selected.all_seller_choice),
        Cancel(Const('❌ Отмена')),
        getter=getters.who_will_transfer,
        state=states.SellerTransferSupervisor.who_will_transfer
    )


async def who_will_take_seller():
    return Window(
        Const('Кому передать?'),
        keyboards.all_sv_for_transfer(
            sv_choice=selected.sv_choice,
        ),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад'))
        ),
        getter=getters.who_will_take_seller,
        state=states.SellerTransferSupervisor.who_will_take_seller,
    )


async def confirm():
    return Window(
        Format("Вы действительно хотите передать сотрудника - {transfer_seller_name}"),
        Format('Управляющему - {transfer_seller_sv_name}?'),
        Button(Const("✅ Передать"), id='confirm_seller_transfer', on_click=selected.confirm),
        Row(
            Cancel(Const('❌ Отмена')),
            Back(Const('⬅️ Назад'))
        ),
        getter=getters.confirm,
        state=states.SellerTransferSupervisor.confirm,
    )

