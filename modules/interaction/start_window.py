from aiogram import types
from aiogram.fsm.context import FSMContext

from modules.interaction.keyboards.keyboards_list import Keyboard
from modules.passive.get_status import is_admin


async def start_window(msg: types.Message, state: FSMContext = None) -> None:
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb1)
    keyboard_admin = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin)
    if not await is_admin(msg):
        await msg.bot.send_message(msg.from_user.id, """Здравствуйте!
Я чат-бот доверия Брянского Машиностроительного Завода.
Здесь Вы можете найти ответы 
на часто задаваемые вопросы или оставить новый запрос, на который Вам ответят представители руководства.
Приятного пользования!""", reply_markup=keyboard)
    else:
        await msg.bot.send_message(msg.from_user.id, """Здравствуйте!
Я чат-бот доверия Брянского Машиностроительного Завода.
Здесь Вы можете найти ответы 
на часто задаваемые вопросы или оставить новый запрос, на который Вам ответят представители руководства.
Приятного пользования!\n"""'Админ', reply_markup=keyboard_admin)