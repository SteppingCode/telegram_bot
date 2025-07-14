from aiogram import types
from aiogram.filters import Command

from modules.interaction.keyboards.keyboards_list import Keyboard
from extra.create_bot import dp


async def help_window(msg: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb4)
    await msg.bot.send_message(msg.chat.id, """Подробно опишите проблему, с которой вы столкнулись.
Укажите причины возникновения проблемы, ее влияние на вашу работу и работу вашего коллектива.
Сформулируйте ваш запрос на решение проблемы четко и конкретно. 
Укажите, какую помощь или какие действия вы хотели бы видеть со стороны начальства для решения проблемы.""",
                               reply_markup=keyboard)


# dp.message.register(help_window, Command('Помощь'))
