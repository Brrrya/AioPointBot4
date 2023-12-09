import aiogram_dialog.api.exceptions
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager, BaseDialogManager, BgManagerFactory
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.shop_dialogs.main_message_dialog import states
from dialogs.shop_dialogs.register_sub_dialog import states as states_register
from dialogs.shop_dialogs.plan_update_dialog import states as states_update_plan

from dialogs.seller_dialogs.main_message_dialog import states as states_seller

from database.shop_requests import ShopRequests


async def go_to_authorization(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(states.MainMessage.auth_wait_badge)


async def take_auth_badge(m: Message, widget: MessageInput, manager: DialogManager):
    shop = await ShopRequests.take_info_about_shop(m.from_user.id)
    worker = await ShopRequests.worker_authorization_on_shop(int(m.text), m.from_user.id)

    if worker:
        if shop['worker_tgid']:
            await manager.bg(shop['worker_tgid'], shop['worker_tgid']).switch_to(states_seller.MainMessageUser.plug)
        if worker['other_shop_tgid']:
            await manager.bg(worker['other_shop_tgid'], worker['other_shop_tgid']).update(data=manager.start_data)
        # if shop['supervisor_tgid']:
        #     await manager.bg(shop['supervisor_tgid'], shop['supervisor_tgid']).update(data=manager.start_data)

        await manager.bg(worker['tgid'], worker['tgid']).start(states_seller.MainMessageUser.main_message)
        await manager.switch_to(states.MainMessage.main_message)
    else:
        await manager.event.answer("Неизвестный бейджик")


async def go_to_registration(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(states_register.MainMessageRegistration.badge_scan)


async def go_to_update_plan(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(states_update_plan.MainMessageUpdatePlan.take_rto)

