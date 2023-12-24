import logging

from aiogram_dialog import DialogManager

from database.requests.director_requests import DirectorRequests


async def fire_choice_sv(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.fire_supervisor.fire_choice_sv>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    data = await DirectorRequests.select_all_supervisors()

    return {
        'supervisors': data
    }


async def fire_confirm(dialog_manager: DialogManager, **kwargs):
    logging.info('Загружено окно <Director.fire_supervisor.fire_confirm>'
                 f' id={dialog_manager.event.from_user.id} username={dialog_manager.event.from_user.username}')

    ctx = dialog_manager.current_context()

    data = await DirectorRequests.select_data_about_fire_sv(ctx.dialog_data.get('fire_sv_tgid'))

    return data
