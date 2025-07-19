from aiogram import types
from aiogram.fsm.context import FSMContext

from modules.passive.get_status import is_admin
from modules.interaction.keyboards.keyboards_list import Keyboard
from modules.interaction.start_window import start_window
from database.connection import db_manager
from modules.interaction.utils import send_media_if_exists

async def show_answer_window(msg: types.Message, state: FSMContext = None):
    data = db_manager.requests.get()
    answered_requests = [req for req in data if req['userId'] == msg.from_user.id and req['answer']]
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin if await is_admin(msg) else Keyboard.kb1)
    for req in answered_requests:
        await msg.bot.send_message(
            msg.chat.id,
            f"Сообщение: {req['message']}\n"
            f"Получено: {req['time']}\n"
            f"Ответ: {req['answer']}\n"
            f"Время ответа: {req['answer_time']}",
            reply_markup=keyboard
        )
        await send_media_if_exists(msg.bot, msg.chat.id, req)

async def hide_answer_window(msg: types.Message, state: FSMContext = None):
    await msg.bot.send_message(msg.chat.id, 'Хорошо, если передумаете, то ваши заявки можно посмотреть командой /my_requests')
    await start_window(msg)