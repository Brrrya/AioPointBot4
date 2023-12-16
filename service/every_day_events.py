import asyncio

import aiogram_dialog.api.exceptions
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram_dialog import DialogManager, StartMode

from database.apscheduler_requests import APScgedulerRequests
from database.plan_requests import PlanRequests

from aiogram_dialog import setup_dialogs

from dialogs.seller_dialogs.main_message_dialog.states import MainMessageUser
from dialogs.shop_dialogs.main_message_dialog.states import MainMessage as MainMessageShop

from service.plan import create_plan

async def not_open_shop_warning(bot: Bot):
    data = await APScgedulerRequests.not_open_shop_warning()

    for sv in data['sv']:
        text = 'Не открылись ещё:\n'
        for shop in data['sv'][sv]:
            text += f'{shop[0]}\n'
        await bot.send_message(sv, str(text))

    for checker in data['checker']:
        text = 'Не открылись ещё:\n'
        for shop in data['checker'][checker]:
            text += shop + '\n'
        await bot.send_message(checker, str(text))

async def who_not_close_shops(bot: Bot):
    data = await APScgedulerRequests.who_not_close_shops()

    for sv in data:
        text = 'Не закрылись ещё:\n'
        for shop in data[sv]:
            text += f'{shop[0]}\n'

        await bot.send_message(sv, str(text))


async def who_not_make_rotate(bot: Bot):
    data = await APScgedulerRequests.who_not_make_rotate()

    for sv in data['sv']:
        text = 'Не сделали ротации ещё:\n'
        for shop in data['sv'][sv]:
            text += f'{shop[0]}\n'
        await bot.send_message(sv, str(text))

    for checker in data['checker']:
        text = 'Не сделали ротации ещё:\n'
        for shop in data['checker'][checker]:
            text += shop + '\n'
        await bot.send_message(checker, str(text))


async def reset_all_shops(setups: setup_dialogs, bot: Bot):
    data = await APScgedulerRequests.reset_all_shops()

    for shop in data['shops']:
        try:
            await setups.bg(bot=bot, chat_id=shop, user_id=shop).update(data={})
        except:
            pass

    for seller in data['sellers']:
        try:
            await setups.bg(bot=bot, chat_id=seller, user_id=seller).start(mode=StartMode.RESET_STACK, state=MainMessageUser.plug)
        except:
            pass


    for supervisor in data['supervisors']:
        try:
            await setups.bg(bot=bot, chat_id=supervisor, user_id=supervisor).update(data={})
        except:
            pass


async def update_all_plans(bot: Bot, setups: setup_dialogs):
    all_shop_data = await APScgedulerRequests.take_all_shop()

    for shop in all_shop_data['all_shops']:
        # формируем старый план для каждого магазина и отправляем его ему
        await create_plan(shop[1])
        await bot.send_document(document=FSInputFile(path=f"../service/plans/{shop[0]}.ods"), chat_id=shop[1])
        await setups.bg(bot=bot, chat_id=shop[1], user_id=shop[1]).done()
        await setups.bg(bot=bot, chat_id=shop[1], user_id=shop[1]).start(MainMessageShop.main_message)
        # Обновляем план в БД для каждого магазина
        await PlanRequests.update_plan(1000000, 100000, 1000, shop[1])


# if __name__ == '__main__':
#     asyncio.run(not_open_shop_warning())

    # for i in res:
    #     for j in res[i]:
    #         print(j[0])



