from aiogram import types
from aiogram.fsm.context import FSMContext

from modules.interaction.keyboards.keyboards_list import Keyboard
from modules.passive.get_status import is_admin


async def admin_panel(msg: types.Message, state: FSMContext = None) -> None:
    if await is_admin(msg):
        keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin_panel)
        await msg.bot.send_message(msg.chat.id, 'Админ панель', reply_markup=keyboard)
    else:
        await msg.bot.send_message(msg.chat.id, 'Вы не сотрудник БМЗ!')