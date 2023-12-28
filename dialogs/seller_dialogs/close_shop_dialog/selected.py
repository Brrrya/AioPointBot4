import datetime
import logging

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from database.requests.plan_requests import PlanRequests
from database.requests.seller_requests import SellerRequests
from dialogs.seller_dialogs.close_shop_dialog.states import MainMessageUserClose


async def close_take_rto(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Ввел выручку РТО - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(close_rto=m.text)
    await manager.switch_to(MainMessageUserClose.close_take_ckp)


async def close_take_ckp(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Ввел выручку ЦКП - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(close_ckp=m.text)
    await manager.switch_to(MainMessageUserClose.close_take_check)


async def close_take_check(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Ввел количество чеков - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(close_check=m.text)
    await manager.switch_to(MainMessageUserClose.close_take_dcart)


async def close_take_dcart(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Ввел количество дисконт. карт - {m.text} id={m.from_user.id} username={m.from_user.username}')

    ctx = manager.current_context()
    ctx.dialog_data.update(close_dcart=m.text)
    await manager.switch_to(MainMessageUserClose.close_take_photos)


async def on_delete_close_photo(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    logging.info(f'Удалил фото id={callback.from_user.id} username={callback.from_user.username}')

    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = dialog_manager.dialog_data.get("photos", [])
    del photos[media_number]
    if media_number > 0:
        await scroll.set_page(media_number - 1)


async def on_input_photo(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    logging.info(f'Вставил фотографию id={message.from_user.id} username={message.from_user.username}')

    dialog_manager.dialog_data.setdefault("photos", []).append(
        (message.photo[-1].file_id, message.photo[-1].file_unique_id),
    )


async def send_report_close_photo(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    logging.info(f'Отправил вечерний отчет id={callback.from_user.id} username={callback.from_user.username}')

    ctx = dialog_manager.current_context()
    photos = ctx.dialog_data.get('photos')
    photos_to_send = []
    for photo in photos:
        photos_to_send.append(photo[0])
    shop = await SellerRequests.take_main_window_info(callback.from_user.id)
    await SellerRequests.insert_photo(callback.from_user.id, 'close', photos_to_send)

    await SellerRequests.save_report(
        rto=int(ctx.dialog_data.get('close_rto')),
        ckp=int(ctx.dialog_data.get('close_ckp')),
        check=int(ctx.dialog_data.get('close_check')),
        dcart=int(ctx.dialog_data.get('close_dcart')),
        shop_tgid=int(shop['shop_tgid']),
        seller_tgid=int(callback.from_user.id)
    )
    await PlanRequests.change_data_in_plan(
        date_for_change=str(datetime.date.today()),
        rto_new_data=int(ctx.dialog_data.get('close_ckp')),
        ckp_new_data=int(ctx.dialog_data.get('close_ckp')),
        check_new_data=int(ctx.dialog_data.get('close_check')),
        dcart_new_data=int(ctx.dialog_data.get('close_dcart')),
        shop_tgid=int(shop['shop_tgid'])
    )

    await dialog_manager.bg(shop['shop_tgid'], shop['shop_tgid']).update(data=dialog_manager.start_data)
    await callback.message.answer('Спасибо за работу! \nМагазин считается закрытым')
    await dialog_manager.done(result={
        'switch_to': 'plug'
    })



