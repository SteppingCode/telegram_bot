from datetime import datetime

from aiogram import types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from modules.interaction.keyboards.keyboards_list import Keyboard
from modules.passive.get_status import is_admin
from database.connection import requests_db
from extra.create_bot import dp


def builder() -> InlineKeyboardBuilder:
    return InlineKeyboardBuilder()


async def list_cmd(msg: types.Message) -> None:
    data = requests_db().get()
    requests = [req for req in data if len(req['answer']) == 0]
    global current_page, max_pages
    current_page = 1
    max_pages = (len(requests) // 5) + 1 if len(requests) % 5 != 0 else (len(requests) // 5)
    if await is_admin(msg):
        keyboard = builder()
        if len(requests) > 0:
            for i in range(1, ((5 * current_page) + 1) if (len(requests) >= 5) else (len(requests)) + 1):
                keyboard.button(text=f"{i} - {requests[i - 1]['message']}",
                                callback_data="info:" + str(requests[i - 1]['id']))
        else:
            keyboard.button(text=f"У вас нету заявок",
                            callback_data=f"requests:empty")
        keyboard.button(text=f"{current_page}/{max_pages}", callback_data=f"current_page:click") if len(
            data) > 0 else None
        keyboard.button(text=f"→", callback_data=f"next:click") if current_page != max_pages and len(
            requests) > 0 else None
        keyboard.button(text='Выйти', callback_data=f"exit:click")
        keyboard.adjust(1, 1, 1, 1, 1, 2, 1)
        await msg.bot.send_message(chat_id=msg.chat.id, text='Список', reply_markup=keyboard.as_markup())
    else:
        await msg.bot.send_message(msg.chat.id, 'Вы не сотрудник БМЗ!')


async def response(call: types.CallbackQuery) -> None:
    data = requests_db().get()
    requests = [req for req in data if len(req['answer']) == 0]
    single_request = requests_db().get(int(call.data.split(':')[1]))
    keyboard = builder()
    if len(requests) > 0:
        for i in range(1 if current_page == 1 else (5 * (current_page - 1)) + 1,
                       (5 * current_page) + 1 if current_page != max_pages else len(requests) + 1):
            keyboard.button(text=f"{i:=^{len(str(i)) + 12}}" if call.data.split(':')[1] == str(
                i) else f"{i} - {requests[i - 1]['message']}",
                            callback_data="info:" + str(requests[i - 1]['id']))
    else:
        keyboard.button(text=f"У вас нету заявок",
                        callback_data=f"requests:empty")
    keyboard.button(text=f"←", callback_data=f"previous:click") if current_page > 1 else None
    keyboard.button(text=f"{current_page}/{max_pages}", callback_data=f"current_page:click")
    keyboard.button(text=f"→", callback_data=f"next:click") if current_page != max_pages else None
    keyboard.button(text=f"Удалить", callback_data="delete:{}".format(*single_request))
    keyboard.button(text=f"Ответить", callback_data="answer:{}".format(int(call.data.split(':')[1])))
    keyboard.button(text='Выйти', callback_data=f"exit:click")
    keyboard.adjust(1, 1, 1, 1, 1, 3, 2, 1) if 1 < current_page < max_pages else keyboard.adjust(1, 1, 1, 1, 1, 2, 2, 1)
    await call.message.edit_text(text='ID: {}\n'
                                      'Message: {}\n'
                                      'Time: {}\n'.format(
        *[single_request[0], single_request[3], single_request[6]])
                                      + (('Answer: {}\n'
                                          'Answer Time: {}'.format(
        *[single_request[7], single_request[8]]) if len(
        single_request[7]) != 0 else f'{"No answer":=^21}')
                                      ),
                                 reply_markup=keyboard.as_markup())
    await call.message.bot.send_message(call.message.chat.id,
                                        f"{single_request[3]} : {single_request[6]}") if len(
        single_request[4]) != 0 or len(
        single_request[5]) != 0 else None
    await call.message.bot.send_photo(call.message.chat.id, single_request[4]) if len(
        single_request[4]) != 0 else None
    await call.message.bot.send_video(call.message.chat.id, single_request[5]) if len(
        single_request[5]) != 0 else None


async def next_click(call: types.CallbackQuery) -> None:
    data = requests_db().get()
    requests = [req for req in data if len(req['answer']) == 0]
    global current_page
    current_page += 1
    keyboard = builder()
    if len(requests) > 0:
        for i in range((5 * (current_page - 1)) + 1,
                       (5 * current_page) + 1 if current_page != max_pages else len(requests) + 1):
            keyboard.button(text=f"{i} - {requests[i - 1]['message']}",
                            callback_data="info:" + str(requests[i - 1]['id']))
    else:
        keyboard.button(text=f"У вас нету заявок",
                        callback_data=f"requests:empty")
    keyboard.button(text=f"←", callback_data=f"previous:click") if current_page > 1 else None
    keyboard.button(text=f"{current_page}/{max_pages}", callback_data=f"current_page:click")
    keyboard.button(text=f"→", callback_data=f"next:click") if current_page != max_pages else None
    keyboard.button(text='Выйти', callback_data=f"exit:click")
    keyboard.adjust(1, 1, 1, 1, 1, 3, 1) if 1 < current_page < max_pages else keyboard.adjust(1, 1, 1, 1, 1, 2, 2, 1)
    await call.message.edit_text(text=call.message.text, reply_markup=keyboard.as_markup())


async def previous_click(call: types.CallbackQuery) -> None:
    data = requests_db().get()
    requests = [req for req in data if len(req['answer']) == 0]
    global current_page
    current_page -= 1
    keyboard = builder()
    if len(requests) > 0:
        for i in range(1 if current_page == 1 else (5 * (current_page - 1)) + 1,
                       (5 * current_page) + 1 if current_page != max_pages else len(requests) + 1):
            keyboard.button(text=f"{i} - {requests[i - 1]['message']}",
                            callback_data="info:" + str(requests[i - 1]['id']))
    else:
        keyboard.button(text=f"У вас нету заявок",
                        callback_data=f"requests:empty")
    keyboard.button(text=f"←", callback_data=f"previous:click") if current_page > 1 else None
    keyboard.button(text=f"{current_page}/{max_pages}", callback_data=f"current_page:click")
    keyboard.button(text=f"→", callback_data=f"next:click") if current_page != max_pages else None
    keyboard.button(text='Выйти', callback_data=f"exit:click")
    keyboard.adjust(1, 1, 1, 1, 1, 3, 1) if 1 < current_page < max_pages else keyboard.adjust(1, 1, 1, 1, 1, 2, 2, 1)
    await call.message.edit_text(text=call.message.text, reply_markup=keyboard.as_markup())


async def delete_request(call: types.CallbackQuery) -> None:
    requests_db().delete(int(call.data.split(":")[1]))
    data = requests_db().get()
    requests = [req for req in data if len(req['answer']) == 0]
    global max_pages, current_page
    max_pages = (len(requests) // 5) + 1 if len(requests) % 5 != 0 else (len(requests) // 5)
    if 5 * max_pages == len(requests):
        current_page = max_pages
    keyboard = builder()
    if len(requests) > 0:
        for i in range(1 if current_page == 1 else (5 * (current_page - 1)) + 1,
                       (5 * current_page) + 1 if current_page != max_pages else len(requests) + 1):
            keyboard.button(text=f"{i} - {requests[i - 1]['message']}",
                            callback_data="info:" + str(requests[i - 1]['id']))
    else:
        keyboard.button(text=f"У вас нету заявок",
                        callback_data=f"requests:empty")
    keyboard.button(text=f"←", callback_data=f"previous:click") if current_page > 1 else None
    keyboard.button(text=f"{current_page}/{max_pages}", callback_data=f"current_page:click")
    keyboard.button(text=f"→", callback_data=f"next:click") if current_page != max_pages else None
    keyboard.button(text='Выйти', callback_data=f"exit:click")
    keyboard.adjust(1, 1, 1, 1, 1, 3, 1) if 1 < current_page < max_pages else keyboard.adjust(1, 1, 1, 1, 1, 2, 2, 1)
    await call.message.edit_text(text='Список', reply_markup=keyboard.as_markup())


class AnswerRequest(StatesGroup):
    get_message = State()


async def answer_handler(call: CallbackQuery, state: FSMContext) -> None:
    keyboard: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin_panel)
    global chosen_request
    chosen_request = int(call.data.split(':')[1])
    await call.message.bot.send_message(call.message.chat.id, "Напишите ответ на сообщение", reply_markup=keyboard)
    await state.set_state(AnswerRequest.get_message)


async def exit_state(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.bot.send_message(call.message.chat.id, "Ок")


async def answer_message(msg: types.Message, state: FSMContext) -> None:
    now: datetime = datetime.now()
    request = requests_db().get(chosen_request)
    requests_db().update(chosen_request, msg.text, f"{now:%y.%m.%d (%H:%M)}")
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_answer)
    await msg.bot.send_message(msg.chat.id, "Ваш ответ добавлен")
    await msg.bot.send_message(request[1], "Вам ответили на сообщение",
                               reply_markup=keyboard)
    await state.clear()


async def exit(call: types.CallbackQuery) -> None:
    await call.message.delete()


dp.callback_query.register(response, F.data.startswith('info:'))
dp.callback_query.register(next_click, F.data.startswith('next:click'))
dp.callback_query.register(previous_click, F.data.startswith('previous:click'))
dp.callback_query.register(delete_request, F.data.startswith("delete:"))
dp.callback_query.register(answer_handler, F.data.startswith('answer:'))
dp.callback_query.register(exit_state, AnswerRequest.get_message, Command('Назад'))
dp.callback_query.register(exit, F.data.startswith("exit:click"))
