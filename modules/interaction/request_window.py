from json import load
from string import punctuation
from datetime import datetime

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from modules.passive.get_status import is_admin
from modules.interaction.keyboards.keyboards_list import Keyboard
from modules.interaction.start_window import start_window
from database.connection import requests_db, questions_db


class RequestWindow(StatesGroup):
    getting_message: State = State()


def limit_messages(user_id: int) -> bool:
    requests = requests_db().get()
    now: datetime = datetime.now()
    today_requests = [req for req in requests if f"{now:%y.%m.%d}" in req['time']]
    user_requests = [user_req for user_req in today_requests if user_req['userId'] == user_id]
    return len(user_requests) >= 3


async def request_window(msg: types.Message, state: FSMContext) -> None:
    if not limit_messages(msg.from_user.id) or await is_admin(msg):
        keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb3)
        await msg.bot.send_message(msg.chat.id, "Опишите Вашу проблему. Добавьте фото или видео, при необходимости.", reply_markup=keyboard)
        await state.set_state(RequestWindow.getting_message)
    else:
        await msg.bot.send_message(msg.chat.id, "Вы превысели дневной лимит сообщений")
        await start_window(msg)


async def exit(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await start_window(msg)


async def get_photo(msg: types.Message, state: FSMContext) -> None:
    file_id = msg.photo[-1].file_id
    await state.update_data(photo_id=file_id)
    await msg.bot.send_message(msg.chat.id, 'Фото получено')


async def get_video(msg: types.Message, state: FSMContext) -> None:
    file_id = msg.video.file_id
    await state.update_data(video_id=file_id)
    await msg.bot.send_message(msg.chat.id, 'Видео получено')


async def response(msg: types.Message, state: FSMContext) -> None:
    await state.update_data(request_text=msg.text.lower())
    questions = questions_db().get()
    quests = [str(i['question']).lower() for i in questions]
    data = await state.get_data()
    if (data['request_text'] not in quests and not {
        i.lower().translate(str.maketrans('', '', punctuation)) for i
        in
        str(data['request_text']).split(' ')}.intersection(
        set(load(open('extra/cenz.json')))) != set()
    ):
        now: datetime = datetime.now()
        await msg.answer(text="Ваш запрос отправлен администратору. Ожидайте ответа.")
        requests_db().add(msg.from_user.id, msg.from_user.username, data['request_text'], data['photo_id'] if 'photo_id' in data else '', data['video_id'] if 'video_id' in data else '', f"{now:%y.%m.%d.%H.%M}")
        await state.clear()
        await start_window(msg)
    else:
        await msg.answer(
            text="Мы не можем передать ваше сообщение по следующим причинам:\n"
                 "‣ Ваше сообщение находится в разделе 'Типовые вопросы'\n"
                 "‣ Ваше сообщение содержит ненормативную лексику\n"
                 "Вам следует переформулировать ваше сообщение."
        )
        await state.clear()
        await start_window(msg)