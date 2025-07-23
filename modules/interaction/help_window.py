from aiogram import types
from modules.interaction.keyboards.keyboards_list import Keyboard


async def help_window(msg: types.Message) -> None:
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb4)
    await msg.bot.send_message(msg.chat.id, """
Подробно опишите проблему, с которой вы столкнулись.\n
Укажите причины возникновения проблемы, ее влияние на вашу работу и работу вашего коллектива.\n
Сформулируйте ваш запрос на решение проблемы четко и конкретно.\n
Укажите, какую помощь или какие действия вы хотели бы видеть со стороны начальства для решения проблемы.\n
""", reply_markup=keyboard)
