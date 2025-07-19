from asyncio import sleep

from aiogram import types
from aiogram.fsm.context import FSMContext

from modules.interaction.keyboards.keyboards_list import Keyboard
from database.connection import db_manager
from modules.passive.get_status import is_admin
from modules.interaction.utils import send_media_if_exists

async def user_requests_window(msg: types.Message, state: FSMContext = None) -> None:
    data = db_manager.requests.get()
    requests = [req for req in data if req['userId'] == msg.from_user.id]
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin if await is_admin(msg) else Keyboard.kb1)
    if requests:
        for req in requests:
            answer_part = (
                f"Ответ: {req['answer']}\n"
                f"Время ответа: {req['answer_time']}"
                if req['answer'] else "Без ответа".center(21, '=')
            )
            await msg.bot.send_message(
                msg.chat.id,
                f"Сообщение: {req['message']}\n"
                f"Получено: {req['time']}\n"
                f"{answer_part}"
            )
            await send_media_if_exists(msg.bot, msg.chat.id, req)
            await sleep(1)
    else:
        await msg.bot.send_message(
            msg.chat.id,
            'У вас нет заявок. Вы можете подать заявку командой /submit_request',
            reply_markup=keyboard
        )