from aiogram import types, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from modules.passive.get_status import is_admin
from modules.interaction.keyboards.keyboards_list import Keyboard
from database.connection import questions_db

from extra.create_bot import dp


class AddFaq(StatesGroup):
    getting_faq = State()
    getting_answer = State()


async def add_faq(msg: types.Message) -> None:
    if await is_admin(msg):
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text=f"Добавить", callback_data=f"add_faq:click")
        keyboard.button(text=f"Удалить", callback_data=f"delete_faq:click")
        keyboard.button(text=f"Выйти", callback_data=f"exit:click")
        keyboard.adjust(1, 1, 1)
        await msg.bot.send_message(msg.chat.id, 'Выберите действие:', reply_markup=keyboard.as_markup())
    else:
        await msg.bot.send_message(msg.chat.id, 'Вы не сотрудник БМЗ!')


async def add_faq_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.bot.send_message(call.message.chat.id, 'Пришлите вопрос')
    await state.set_state(AddFaq.getting_faq)


async def exit_state(msg: types.Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin_panel)
    await state.clear()
    await msg.bot.send_message(msg.chat.id, 'Как пожелаете', reply_markup=keyboard)


async def get_faq(msg: types.Message, state: FSMContext) -> None:
    quest = msg.text
    await state.update_data(question=quest)
    await state.set_state(AddFaq.getting_answer)
    await msg.bot.send_message(msg.chat.id, 'Теперь ответ')


async def get_answer(msg: types.Message, state: FSMContext) -> None:
    answer = msg.text
    await state.update_data(answer=answer)
    data = await state.get_data()
    questions_db().add(data['question'], data['answer'])
    await state.clear()
    await msg.bot.send_message(msg.chat.id, 'Список типовых вопросов был обновлен!')
    await add_faq(msg)


async def delete_faq_callback(call: CallbackQuery) -> None:
    questions = questions_db().get()
    if len(questions) != 0:
        keyboard = InlineKeyboardBuilder()
        for i in range(1, len(questions)+1):
            keyboard.button(text=f"{i} - {questions[i-1][1]}: {questions[i-1][2]}", callback_data=f"delete_question:{i}")
        keyboard.button(text=f"Выйти", callback_data=f"exit:click")
        keyboard.adjust(1, repeat=True)
        await call.message.bot.send_message(call.message.chat.id, text="Список вопросов, выберите который из них нужно удалить", reply_markup=keyboard.as_markup())
        InlineKeyboardBuilder().buttons.close()
    else:
        await call.message.bot.send_message(call.message.chat.id, 'Список пуст')


async def delete_question_callback(call: CallbackQuery) -> None:
    deleted = questions_db().delete(questions_db().get()[int(call.data.split(':')[1]) - 1]['id'])
    questions = questions_db().get()
    keyboard = InlineKeyboardBuilder()
    if len(questions) > 0:
        for i in range(1, len(questions)+1):
            keyboard.button(text=f"{i} - {questions[i-1][1]}: {questions[i-1][2]}", callback_data=f"delete_question:{i}")
        keyboard.button(text=f"Выйти", callback_data=f"exit:click")
        keyboard.adjust(1, repeat=True)
    else:
        keyboard = InlineKeyboardBuilder()
    await call.message.edit_text(call.message.text, reply_markup=keyboard.as_markup())
    await call.message.bot.send_message(call.message.chat.id, 'Список типовых вопросов был обновлен!' if deleted else 'Ошибка')
    InlineKeyboardBuilder().buttons.close()


async def exit_faq_callback(call: CallbackQuery) -> None:
    await call.message.delete()
    await call.message.bot.send_message(call.message.chat.id, 'Ок')


dp.callback_query.register(add_faq_callback, F.data.startswith('add_faq:click'))
dp.callback_query.register(delete_faq_callback, F.data.startswith('delete_faq:click'))
dp.callback_query.register(delete_question_callback, F.data.startswith('delete_question:'))
dp.callback_query.register(exit_faq_callback, F.data.startswith('exit:click'))
