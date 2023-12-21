import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.seller_dialogs.main_message_dialog import states as states_main_message
from dialogs.seller_dialogs.close_shop_dialog import states as states_close_dialog

from database.requests.seller_requests import SellerRequests


async def checker_command(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Ввёл команду проверяющего {m.text} id={m.from_user.id} username={m.from_user.username}')
    if m.text == '/open':
        data = await SellerRequests.checker_all_photo_open(int(m.from_user.id))
    else:
        data = await SellerRequests.checker_all_photo_rotate(int(m.from_user.id))

    for photo in data['all_photo']:
        await m.answer_photo(photo=photo[0], caption=photo[1])

    if data['all_make_action'] is True:
        if m.text == '/open':
            await m.answer('Все магазины закрепленные за вами открыты!')
        elif m.text == '/rotate':
            await m.answer('Все магазины закрепленные за вами сделали ротации!')
    else:
        text = 'Ещё не открылись:\n' if m.text == '/open' else 'Ещё не сделали ротации:\n'
        for shop_name in data['who_not_do']:
            text += f'{shop_name[0]}\n'
        await m.answer(text)

    # await m.answer(m.text[1::])

async def to_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Перешёл по кнопке в main_window id={c.from_user.id} username={c.from_user.username}')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def open_button(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Нажал кнопку открытия id={c.from_user.id} username={c.from_user.username}')
    await manager.switch_to(states_main_message.MainMessageUser.open_photo)


async def open_photo(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Отправил фото чека открытия id={m.from_user.id} username={m.from_user.username}')
    ctx = manager.current_context()
    ctx.dialog_data.update(open_photo=m.photo[-1].file_id)
    await manager.switch_to(states_main_message.MainMessageUser.open_photo_confirm)


async def open_photo_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Подтвердил фото открытия id={c.from_user.id} username={c.from_user.username}')
    ctx = manager.current_context()
    await SellerRequests.insert_photo(c.from_user.id, 'open', [ctx.dialog_data.get('open_photo')])
    shop = await SellerRequests.take_main_window_info(c.from_user.id)
    await manager.bg(shop['shop_tgid'], shop['shop_tgid']).update(data=manager.start_data)
    await c.message.answer('Сохранено!')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def rotate_button(c: CallbackQuery, widget: MessageInput, manager: DialogManager):
    logging.info(f'Нажал кнопку ротаций id={c.from_user.id} username={c.from_user.username}')
    await manager.switch_to(states_main_message.MainMessageUser.rotate_photo)


async def rotate_photo(m: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(rotate_photo=m.photo[-1].file_id)
    await manager.switch_to(states_main_message.MainMessageUser.rotate_photo_confirm)


async def rotate_photo_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Подтвердил фото ротаций id={c.from_user.id} username={c.from_user.username}')
    ctx = manager.current_context()
    await SellerRequests.insert_photo(c.from_user.id, 'rotate', [ctx.dialog_data.get('rotate_photo')])
    shop = await SellerRequests.take_main_window_info(c.from_user.id)
    await manager.bg(shop['shop_tgid'], shop['shop_tgid']).update(data=manager.start_data)
    await c.message.answer('Сохранено!')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def close_button(c: CallbackQuery, widget: MessageInput, manager: DialogManager):
    logging.info(f'Нажал кнопку закрытия id={c.from_user.id} username={c.from_user.username}')
    await manager.start(states_close_dialog.MainMessageUserClose.close_take_rto)

