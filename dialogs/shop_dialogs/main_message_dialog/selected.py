import logging

from aiogram.types import CallbackQuery, Message, FSInputFile

from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from dialogs.shop_dialogs.main_message_dialog import states
from dialogs.shop_dialogs.register_sub_dialog import states as states_register
from dialogs.shop_dialogs.plan_update_dialog import states as states_update_plan
from dialogs.seller_dialogs.main_message_dialog import states as states_seller
from dialogs.shop_dialogs.plan_change_dialog import states as states_change_plan


from database.requests.shop_requests import ShopRequests
from service import plan

async def go_to_authorization(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Магазин | Нажата кнопка авторизации id={c.from_user.id} username={c.from_user.username}')

    await manager.switch_to(states.MainMessage.auth_wait_badge)


async def take_auth_badge(m: Message, widget: MessageInput, manager: DialogManager):
    logging.info(f'Магазин | Отправили бейдж - {m.text} id={m.from_user.id} username={m.from_user.username}')

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
    logging.info(f'Магазин | Нажал кнопку регистрации id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_register.MainMessageRegistration.badge_scan)


async def go_to_update_plan(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Магазин | Нажал кнопку обновления плана id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_update_plan.MainMessageUpdatePlan.take_rto)


async def get_plan(c: CallbackQuery, widget: Button, manager: DialogManager):
    logging.info(f'Магазин | Нажал кнопку получения плана id={c.from_user.id} username={c.from_user.username}')

    await plan.create_plan(c.from_user.id)
    data = await ShopRequests.take_info_about_shop(c.from_user.id)
    await c.message.answer_document(document=FSInputFile(path=f"../service/plans/{data['title']}.ods"))

    await manager.reset_stack()
    await manager.start(mode=StartMode.RESET_STACK, state=states.MainMessage.main_message)


async def change_plan_button(c: CallbackQuery, widget: MessageInput, manager: DialogManager):
    logging.info(f'Магазин | Нажал кнопку изменить план id={c.from_user.id} username={c.from_user.username}')

    await manager.start(states_change_plan.MainMessageChangePlan.take_date_for_change)
