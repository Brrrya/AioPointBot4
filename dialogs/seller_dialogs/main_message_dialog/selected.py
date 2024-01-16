import logging

from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from database.requests.unknown_requests import UnknownRequests
from dialogs.seller_dialogs.main_message_dialog import states as states_main_message
from dialogs.seller_dialogs.close_shop_dialog import states as states_close_dialog

from database.requests.seller_requests import SellerRequests


async def register_command(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Продавец | Ввёд команду /register id={m.from_user.id} username={m.from_user.username}')

    await manager.switch_to(states_main_message.MainMessageUser.register_command)


async def register_command_code(message: Message, widget: MessageInput, manager: DialogManager):
    """Ловит введенный код регистрации после команды /register"""
    logging.info(f'Продавец | Ввел код регистрации - {message.text} id={message.from_user.id} username={message.from_user.username}')
    try:
        if await UnknownRequests.select_register_user_by_reg_code(int(message.text), int(message.from_user.id)):
            logging.info(f'Успешно зарегистрирован id={message.from_user.id} username={message.from_user.username}')
            await message.answer("Вы успешно зарегистрировались!")
            await manager.switch_to(states_main_message.MainMessageUser.plug)

        else:
            logging.info(f'Неверный код регистрации id={message.from_user.id} username={message.from_user.username}')
            await message.answer("Регистрационный код не найден")
            await manager.switch_to(states_main_message.MainMessageUser.register_command)
    except ValueError:
        logging.info(f'Неверный формат регистрационного кода id={message.from_user.id} username={message.from_user.username}')
        await message.answer("Неверный формат регистрационного кода")
        await manager.switch_to(states_main_message.MainMessageUser.register_command)


async def checker_command(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Продавец | Ввёл команду проверяющего {m.text} id={m.from_user.id} username={m.from_user.username}')

    # потом все надо зарефакторить

    if m.text == '/open':
        data = await SellerRequests.checker_all_photo_open(int(m.from_user.id))
    elif m.text == '/rotate':
        data = await SellerRequests.checker_all_photo_rotate(int(m.from_user.id))
    elif m.text == '/close':
        all_data = await SellerRequests.checker_reports(int(m.from_user.id))
        keys = all_data.keys()
        close_data = await SellerRequests.checker_report_who_not_send(m.from_user.id)

    if m.text == '/open' or m.text == '/rotate':
        for photo in data['all_photo']:
            await m.answer_photo(photo=photo[0], caption=photo[1])
    else:
        for key in keys:
            text = ''
            text += f'Магазин - {all_data[key]["shop_name"]}\n'
            text += f'Сотрудник - {all_data[key]["seller_name"]}\n'
            text += f'РТО - {all_data[key]["rto"]} / {all_data[key]["p_rto"]}\n'
            text += f'ЦКП - {all_data[key]["ckp"]} / {all_data[key]["p_ckp"]}\n'
            text += f'Чеки - {all_data[key]["check"]} / {all_data[key]["p_check"]}\n'
            text += f'Дисконт. карты - {all_data[key]["dcart"]}\n'

            media = MediaGroupBuilder()
            for photo in all_data[key]['photos']:
                media.add_photo(photo)

            await m.answer(text)
            await m.answer_media_group(media.build())

    if m.text == '/open' or m.text == '/rotate':
        if data['all_make_action'] is True:
            if m.text == '/open':
                await m.answer('Все магазины закрепленные за вами открыты!')
            elif m.text == '/rotate':
                await m.answer('Все магазины закрепленные за вами сделали ротации!')
        elif data['all_make_action'] is False:
            text = 'Ещё не открылись:\n' if m.text == '/open' else 'Ещё не сделали ротации:\n'
            for shop_name in data['who_not_do']:
                text += f'{shop_name[0]}\n'
            await m.answer(text)
    elif m.text == '/close':
        text = 'Все магазины закрепленные за вами закрыты!'
        if close_data['close_report_or_not'] is False:
            text = 'Ещё не закрылись:\n'
            for shop_name in close_data['all_not_close_report']:
                text += f'{shop_name[0]}\n'
        await m.answer(text)


async def to_plug(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Продавец | Перешёл по кнопке в plug id={c.from_user.id} username={c.from_user.username}')
    await manager.switch_to(states_main_message.MainMessageUser.plug)


async def to_main_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Продавец | Перешёл по кнопке в main_window id={c.from_user.id} username={c.from_user.username}')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def open_button(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Продавец | Нажал кнопку открытия id={c.from_user.id} username={c.from_user.username}')
    await manager.switch_to(states_main_message.MainMessageUser.open_photo)


async def open_photo(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Продавец | Отправил фото чека открытия id={m.from_user.id} username={m.from_user.username}')
    ctx = manager.current_context()
    ctx.dialog_data.update(open_photo=m.photo[-1].file_id)
    await manager.switch_to(states_main_message.MainMessageUser.open_photo_confirm)


async def open_photo_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Продавец | Подтвердил фото открытия id={c.from_user.id} username={c.from_user.username}')
    ctx = manager.current_context()
    await SellerRequests.insert_photo(c.from_user.id, 'open', [ctx.dialog_data.get('open_photo')])
    shop = await SellerRequests.take_main_window_info(c.from_user.id)
    await manager.bg(shop['shop_tgid'], shop['shop_tgid']).update(data=manager.start_data)
    await c.message.answer('Сохранено!')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def rotate_button(c: CallbackQuery, widget: MessageInput, manager: DialogManager):
    logging.info(f'Продавец | Нажал кнопку ротаций id={c.from_user.id} username={c.from_user.username}')
    await manager.switch_to(states_main_message.MainMessageUser.rotate_photo)


async def rotate_photo(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Продавец | Отправил фото ротаций id={m.from_user.id} username={m.from_user.username}')
    ctx = manager.current_context()
    ctx.dialog_data.update(rotate_photo=m.photo[-1].file_id)
    await manager.switch_to(states_main_message.MainMessageUser.rotate_photo_confirm)


async def rotate_photo_confirm(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Продавец | Подтвердил фото ротаций id={c.from_user.id} username={c.from_user.username}')
    ctx = manager.current_context()
    await SellerRequests.insert_photo(c.from_user.id, 'rotate', [ctx.dialog_data.get('rotate_photo')])
    shop = await SellerRequests.take_main_window_info(c.from_user.id)
    await manager.bg(shop['shop_tgid'], shop['shop_tgid']).update(data=manager.start_data)
    await c.message.answer('Сохранено!')
    await manager.switch_to(states_main_message.MainMessageUser.main_message)


async def close_button(c: CallbackQuery, widget: MessageInput, manager: DialogManager):
    logging.info(f'Продавец | Нажал кнопку закрытия id={c.from_user.id} username={c.from_user.username}')

    ctx = manager.current_context()

    await manager.start(states_close_dialog.MainMessageUserClose.close_take_rto,
                        data={'shop_tgid': ctx.dialog_data.get('shop_tgid')})

