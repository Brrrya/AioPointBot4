from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format, Const, Case, Multi
from aiogram_dialog.widgets.kbd import Back, Next, Button
from aiogram_dialog.widgets.input import MessageInput

from aiogram_dialog.widgets.kbd import Cancel

from dialogs.shop_dialogs.register_sub_dialog import (
    getters, keyboards, selected, states
)


async def scan_new_worker_badge():
    return Window(
        Const('Сканируйте бейджик нового сотрудника'),
        MessageInput(selected.take_register_badge, filter=lambda message: message.text.isdigit()),
        Cancel(Const('❌️ Отмена')),
        getter=getters.scan_new_worker_badge,
        state=states.MainMessageRegistration.badge_scan
    )


async def take_first_name():
    return Window(
        Format('Имя - '),
        Format('Фамилия - '),
        Format('Супервайзер - '),
        Const(' '),
        Const('Введите имя сотрудника'),
        Back(Const('⬅️ Назад')),
        Cancel(Const('❌ Отмена')),
        MessageInput(selected.take_first_name),
        getter=getters.take_first_name,
        state=states.MainMessageRegistration.enter_f_name
    )


async def take_last_name():
    return Window(
        Format('Имя - {first_name}'),
        Format('Фамилия - '),
        Format('Супервайзер - '),
        Const(' '),
        Const('Введите фамилию сотрудника'),
        Back(Const('⬅️ Назад')),
        Cancel(Const('❌ Отмена')),
        MessageInput(selected.take_last_name),
        getter=getters.take_last_name,
        state=states.MainMessageRegistration.enter_l_name
    )


async def take_supervisor():
    return Window(
        Format('Имя - {first_name}'),
        Format('Фамилия - {last_name}'),
        Format('Супервайзер - '),
        Const(' '),
        Const('Выберете вашего супервайзера'),
        keyboards.take_supervisor(selected.take_supervisor),
        Back(Const('⬅️ Назад')),
        Cancel(Const('❌ Отмена')),
        getter=getters.take_all_supervisor,
        state=states.MainMessageRegistration.enter_supervisor
    )


async def confirm_data():
    return Window(
        Format('Имя - {first_name}'),
        Format('Фамилия - {last_name}'),
        Format('Супервайзер - {supervisor}'),
        Const(' '),
        Const('Все данные верны?'),
        Button(Const('Все верно'), on_click=selected.confirm_data, id='confirm_register_new_user'),
        Back(Const('⬅️ Назад')),
        Cancel(Const('❌ Отмена')),
        getter=getters.confirm_data,
        state=states.MainMessageRegistration.confirm
    )


async def register_code():
    return Window(
        Format('Ваш код регистрации - {reg_code}'),
        Const(' '),
        Const('Зайдите в бота со своего личного телефона, напишите команду /register '
              'и впишите свой код регистрации.'),
        Const('Ссылка на бота @point_manager_bot'),
        Const(' '),
        Const('ВНИМАНИЕ'),
        Const('Регистрироваться надо всего один раз. НЕ НАДО регистрироваться на каждом магазине.'),
        Button(Const('✅ Завершить'), on_click=selected.coplete_register, id='complete_register_new_user'),
        getter=getters.register_code,
        state=states.MainMessageRegistration.register_code
    )
