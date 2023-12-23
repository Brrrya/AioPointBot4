from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Row
from aiogram_dialog.widgets.text import Format, Const

from dialogs.supervisor_dialogs.change_checker_dialog import (
    getters, keyboards, selected, states
)


async def select_role_checker():
    return Window(
        Const('Проверяющий - '),
        Const('Магазин - '),
        Const('Новый проверяющий - '),
        Const(' '),
        Const('Какого проверяющего поменять?'),
        Row(
            Button(Const('Открытие'), id='change_open_checker', on_click=selected.change_open),
            Button(Const('Ротации'), id='change_rotate_checker', on_click=selected.change_rotate),
        ),
        Cancel(Const('Отмена')),
        getter=getters.select_role_checker,
        state=states.ChangeCheckerSupervisor.select_role
    )


async def select_shop_checker():
    return Window(
        Format('Проверяющий - {checker_role}'),
        Const('Магазин - '),
        Const('Новый проверяющий - '),
        Const(' '),
        Format('На каком магазине поменять проверяющего {checker_role}?'),
        keyboards.select_shop_checker(
            on_click=selected.select_shop_checker
        ),
        Row(
            Cancel(Const('Отмена')),
            Back(Const('Назад'))
        ),
        getter=getters.select_shop_checker,
        state=states.ChangeCheckerSupervisor.select_shop
    )


async def select_seller_checker():
    return Window(
        Format('Проверяющий - {checker_role}'),
        Format('Магазин - {checker_shop}'),
        Const('Новый проверяющий - '),
        Const(' '),
        Format('Какого проверяющего {checker_role} определить на магазин {checker_shop}?'),
        Button(Const('Убрать проверяющего'), id='select_seller_checker_remove', on_click=selected.remove_seller_checker),
        keyboards.select_seller_checker(
            on_click=selected.select_seller_checker
        ),
        Row(
            Cancel(Const('Отмена')),
            Back(Const('Назад'))
        ),
        getter=getters.select_seller_checker,
        state=states.ChangeCheckerSupervisor.select_new_checker
    )


async def confirm():
    return Window(
        Format('Проверяющий - {checker_role}'),
        Format('Магазин - {checker_shop}'),
        Format('Новый проверяющий - {new_checker}'),
        Const(' '),
        Const('Всё верно?'),
        Button(Const('Да'), id='confirm_new_checker', on_click=selected.confirm_new_checker),
        Row(
            Cancel(Const('Отмена')),
            Back(Const('Назад'))
        ),
        getter=getters.confirm,
        state=states.ChangeCheckerSupervisor.confirm
    )

