from aiogram import Bot
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from service import every_day_events


async def create_tasks(bot: Bot, setups: setup_dialogs):
    # Временную зону устанавливаем
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    # Список всех запланированных задач
    scheduler.add_job(every_day_events.not_open_shop_warning, trigger='cron',
                      hour='08', minute='50', kwargs={'bot': bot})  # предупреждение о не открытых
    scheduler.add_job(every_day_events.who_not_close_shops, trigger='cron',
                      hour='23', minute='00', kwargs={'bot': bot})  # предупреждение о не закрытых
    scheduler.add_job(every_day_events.who_not_make_rotate, trigger='cron',
                      hour='18', minute='00', kwargs={'bot': bot})  # предупреждение о не сделавших ротации
    scheduler.add_job(every_day_events.reset_all_shops, trigger='cron',
                      hour='00', minute='05', kwargs={'setups': setups, 'bot': bot})  # обнуление всех магазинов
    scheduler.add_job(every_day_events.update_all_plans, trigger='cron',
                      day='01', hour='00', minute='10', kwargs={'setups': setups, 'bot': bot})  # Обновление планов

    scheduler.start()


