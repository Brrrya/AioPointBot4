from aiogram import F

from aiogram_dialog import Window, DialogManager, Data

from aiogram_dialog.widgets.text import Format, Const, List, Multi, Case
from aiogram_dialog.widgets.kbd import Back, Button, Cancel
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.media.static import ContentType
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia


from dialogs.supervisor_dialogs.shop_transfer_dialog import (
    getters, keyboards, selected, states
)


async def who_will_transfer_shop():
    return Window(
        Case(
            {
                True:
                    Const("Какой магазин передать?"),
                False:
                    Const('За вами не закреплен ни один магазин')
            },
            selector='more_then_nobody'
        ),
        keyboards.all_shops_by_sv(
            shop_choice=selected.shop_choice,
        ),
        Button(Const("Все"), id='all_shops_choice_for_transfer',
               when='more_then_nobody', on_click=selected.all_shop_choice),
        Cancel(Const('Отмена')),
        getter=getters.who_will_transfer_shop,
        state=states.ShopTransferSupervisor.who_will_transfer_shop
    )


async def who_will_take_shop():
    return Window(
        Const('Кому передать?'),
        keyboards.all_sv_for_transfer(
            sv_choice=selected.sv_choice,
        ),
        Back(Const('Назад')),
        Cancel(Const('Отмена')),
        getter=getters.who_will_take_shop,
        state=states.ShopTransferSupervisor.who_will_take_shop,
    )


async def confirm():
    return Window(
        Format("Вы действительно хотите передать магазин - {transfer_shop_title}"),
        Format('Управляющему - {transfer_shop_sv_name}?'),
        Button(Const("Передать"), id='confirm_shop_transfer', on_click=selected.confirm),
        Back(Const("Назад")),
        Cancel(Const("Отмена")),
        getter=getters.confirm,
        state=states.ShopTransferSupervisor.confirm,
    )

