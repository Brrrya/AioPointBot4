import logging
import datetime

from aiogram.enums import ContentType

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.common import ManagedScroll

from database.requests.plan_requests import PlanRequests


async def close_take_rto(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.close_shop.close_take_rto>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()
    plan_data = await PlanRequests.take_plan_one_day(date_=datetime.date.today(), shop_tgid=int(ctx.start_data.get('shop_tgid')))

    ctx.dialog_data.update(rto_plan=plan_data['rto_plan'],
                           ckp_plan=plan_data['ckp_plan'],
                           check_plan=plan_data['check_plan'])

    return {
        'rto_plan': ctx.dialog_data.get('rto_plan'),
        'ckp_plan': ctx.dialog_data.get('ckp_plan'),
        'check_plan': ctx.dialog_data.get('check_plan'),
    }


async def close_take_ckp(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.close_shop.close_take_ckp>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'close_rto': ctx.dialog_data.get('close_rto'),
        'rto_plan': ctx.dialog_data.get('rto_plan'),
        'ckp_plan': ctx.dialog_data.get('ckp_plan'),
        'check_plan': ctx.dialog_data.get('check_plan'),
    }


async def close_take_check(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.close_shop.close_take_check>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'close_rto': ctx.dialog_data.get('close_rto'),
        'close_ckp': ctx.dialog_data.get('close_ckp'),
        'rto_plan': ctx.dialog_data.get('rto_plan'),
        'ckp_plan': ctx.dialog_data.get('ckp_plan'),
        'check_plan': ctx.dialog_data.get('check_plan'),
    }


async def close_take_dcart(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.close_shop.close_take_dcart>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()
    return {
        'close_rto': ctx.dialog_data.get('close_rto'),
        'close_ckp': ctx.dialog_data.get('close_ckp'),
        'close_check': ctx.dialog_data.get('close_check'),
        'rto_plan': ctx.dialog_data.get('rto_plan'),
        'ckp_plan': ctx.dialog_data.get('ckp_plan'),
        'check_plan': ctx.dialog_data.get('check_plan'),
    }


async def close_take_photos(dialog_manager: DialogManager, **kwargs):
    logging.info(f'Загружено окно <Seller.close_shop.close_take_photos>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')
    ctx = dialog_manager.current_context()

    scroll: ManagedScroll = dialog_manager.find("pages")
    media_number = await scroll.get_page()
    photos = dialog_manager.dialog_data.get("photos", [])
    if photos:
        photo = photos[media_number]
        media = MediaAttachment(
            file_id=MediaId(*photo),
            type=ContentType.PHOTO,
        )
    else:
        media = MediaAttachment(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/800px-Image_not_available.png?20210219185637",
            type=ContentType.PHOTO,
        )

    return {
        'close_rto': ctx.dialog_data.get('close_rto'),
        'close_ckp': ctx.dialog_data.get('close_ckp'),
        'close_check': ctx.dialog_data.get('close_check'),
        'close_dcart': ctx.dialog_data.get('close_dcart'),
        'rto_plan': ctx.dialog_data.get('rto_plan'),
        'ckp_plan': ctx.dialog_data.get('ckp_plan'),
        'check_plan': ctx.dialog_data.get('check_plan'),
        "media_count": len(photos),
        "media_number": media_number + 1,
        "media": media,
    }

