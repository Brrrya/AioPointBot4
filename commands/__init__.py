__all__ = ['start', 'register_user_commands', 'bot_commands', 'help']

from aiogram import Router, F
from aiogram.filters import Command, StateFilter

from commands.start import start
from commands.help import help_command
from commands.register import register_command, register_command_check_reg_code, my_state

from states.states import UnknownFSM

from filters import unknown_filters


def register_user_commands(router: Router) -> None:
    """Регистрация всех команд вне диалога"""
    router.message.register(start, Command(commands=['start']))
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(register_command, Command(commands=['register']), unknown_filters.RegisterFilter())
    router.message.register(register_command_check_reg_code, StateFilter(UnknownFSM.wait_reg_code))
    router.message.register(my_state, Command(commands=['mystate']))
