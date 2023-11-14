import time
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp

from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, MenuButtonWebApp

from bot.commands import get_admin_commands, get_default_commands
from loader import dp, _, bot
from models import User


@dp.message_handler(CommandStart())
async def _start(message: Message, user: User):
    web_app_uri = 'https://katrine.uz'
    web_app_uri += '?time=' + str(time.time())

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton('Menu', web_app=WebAppInfo(url=web_app_uri + '&keyboard_button=1'))
    )

    await message.answer('Web app', reply_markup=markup)
    await bot.set_chat_menu_button(message.chat.id, MenuButtonWebApp(text='Menu', web_app=WebAppInfo(url=web_app_uri)))


@dp.message_handler(i18n_text='Help 🆘')
@dp.message_handler(CommandHelp())
async def _help(message: Message, user: User):
    commands = get_admin_commands(user.language) if user.is_admin else get_default_commands(user.language)

    text = _('Help 🆘') + '\n\n'
    for command in commands:
        text += f'{command.command} - {command.description}\n'

    await message.answer(text)
