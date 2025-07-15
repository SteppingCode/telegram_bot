from aiogram import types
from aiogram.fsm.context import FSMContext

from modules.passive.get_status import is_admin
from modules.interaction.keyboards.keyboards_list import Keyboard
from modules.interaction.start_window import start_window
from database.connection import db_manager


async def show_answer_window(msg: types.Message, state: FSMContext = None):
    data = db_manager.requests.get()
    answered_requests = [req for req in data if req['userId'] == msg.from_user.id and len(req['answer']) != 0]
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin if await is_admin(msg) else Keyboard.kb1)
    for i in range(len(answered_requests)):
        await msg.bot.send_message(msg.chat.id, 'Message: {}\n'
                                                'MessageTime: {}\n'
                                                'Answer: {}\n'
                                                'AnswerTime: {}'.format(answered_requests[i]['message'],
                                                                        answered_requests[i]['time'],
                                                                        answered_requests[i]['answer'],
                                                                        answered_requests[i]['answer_time']),
                                   reply_markup=keyboard)
        await msg.bot.send_photo(msg.chat.id, answered_requests[i]['photo_id']) if len(answered_requests[i]['photo_id']) != 0 else None
        await msg.bot.send_video(msg.chat.id, answered_requests[i]['video_id']) if len(answered_requests[i]['video_id']) != 0 else None


async def hide_answer_window(msg: types.Message, state: FSMContext = None):
    await msg.bot.send_message(msg.chat.id, 'Хорошо, если передумаете, то ваши заявки можно посмотреть в разделе <Мои Заявки>')
    await start_window(msg)