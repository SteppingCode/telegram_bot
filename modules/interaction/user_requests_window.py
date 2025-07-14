from aiogram import types

from modules.interaction.keyboards.keyboards_list import Keyboard
from database.connection import requests_db
from modules.passive.get_status import is_admin


async def user_requests_window(msg: types.Message) -> None:
    data = requests_db().get()
    requests = [req for req in data if req['userId'] == msg.from_user.id]
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin if await is_admin(msg) else Keyboard.kb1)
    if len(requests) > 0:
        for i in range(len(requests)):
            await msg.bot.send_message(msg.chat.id, 'Message: {}\n'
                                                    'MessageTime: {}\n'.format(requests[i]['message'], requests[i]['time'])
                                                    + (('Answer: {}\n'
                                                        'AnswerTime: {}').format(requests[i]['answer'], requests[i]['answer_time']) if len(requests[i]['answer']) != 0 else f'{"No answer":=^21}'))
            await msg.bot.send_photo(msg.chat.id, requests[i]['photo_id']) if len(requests[i]['photo_id']) != 0 else None
            await msg.bot.send_video(msg.chat.id, requests[i]['video_id']) if len(requests[i]['video_id']) != 0 else None
    else:
        await msg.bot.send_message(msg.chat.id, 'У вас нет заявок. Вы можете подать заявку в разделе <Подать заявку>', reply_markup=keyboard)