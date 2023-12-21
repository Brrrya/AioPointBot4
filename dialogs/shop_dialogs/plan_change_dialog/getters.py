from aiogram_dialog import DialogManager


async def change_take_rto(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
    }


async def change_take_ckp(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
    }


async def change_take_check(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
        'ckp_new_data': ctx.dialog_data.get('ckp_new_data')
    }


async def change_take_dcart(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
        'ckp_new_data': ctx.dialog_data.get('ckp_new_data'),
        'check_new_data': ctx.dialog_data.get('check_new_data')
    }


async def confirm(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {
        'date_for_change': ctx.dialog_data.get('date_for_change'),
        'rto_old_data': ctx.dialog_data.get('rto_old_data'),
        'ckp_old_data': ctx.dialog_data.get('ckp_old_data'),
        'check_old_data': ctx.dialog_data.get('check_old_data'),
        'dcart_old_data': ctx.dialog_data.get('dcart_old_data'),
        'rto_new_data': ctx.dialog_data.get('rto_new_data'),
        'ckp_new_data': ctx.dialog_data.get('ckp_new_data'),
        'check_new_data': ctx.dialog_data.get('check_new_data'),
        'dcart_new_data': ctx.dialog_data.get('dcart_new_data'),
    }




