from aiogram import types, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from modules.interaction.start_window import start_window
from modules.passive.get_status import is_admin
from modules.interaction.keyboards.keyboards_list import Keyboard
from database.connection import db_manager

from extra.create_bot import dp

class AddFaq(StatesGroup):
    getting_faq = State()
    getting_answer = State()

def _build_inline_keyboard(buttons: list[tuple[str, str]]) -> types.InlineKeyboardMarkup:
    """Build an inline keyboard with the given buttons (text, callback_data pairs)."""
    keyboard = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        keyboard.button(text=text, callback_data=callback_data)
    keyboard.adjust(1, repeat=True)
    return keyboard.as_markup()

def _build_faq_keyboard(questions: list) -> types.InlineKeyboardMarkup:
    """Build an inline keyboard for FAQ questions, with an exit button."""
    if not questions:
        return InlineKeyboardBuilder().as_markup()
    buttons = [(f"{i} - {q[1]}: {q[2]}", f"delete_question:{i}") for i, q in enumerate(questions, 1)]
    buttons.append(("Выйти", "exit:click"))
    return _build_inline_keyboard(buttons)

async def add_faq(msg: types.Message, state: FSMContext = None) -> None:
    if await is_admin(msg):
        buttons = [
            ("Добавить", "add_faq:click"),
            ("Удалить", "delete_faq:click"),
            ("Выйти", "exit:click"),
        ]
        keyboard = _build_inline_keyboard(buttons)
        await msg.bot.send_message(msg.chat.id, 'Выберите действие:', reply_markup=keyboard)
    else:
        await msg.bot.send_message(msg.chat.id, 'Вы не сотрудник БМЗ!')

async def add_faq_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.bot.send_message(call.message.chat.id, 'Пришлите вопрос')
    await state.set_state(AddFaq.getting_faq)

async def exit_state(msg: types.Message, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin_panel)
    await state.clear()
    await msg.bot.send_message(msg.chat.id, 'Как пожелаете', reply_markup=keyboard)
    await start_window(msg)

async def get_faq(msg: types.Message, state: FSMContext) -> None:
    quest = msg.text
    await state.update_data(question=quest)
    await state.set_state(AddFaq.getting_answer)
    await msg.bot.send_message(msg.chat.id, 'Теперь ответ')

async def get_answer(msg: types.Message, state: FSMContext) -> None:
    answer = msg.text
    await state.update_data(answer=answer)
    data = await state.get_data()
    db_manager.questions.add(data['question'], data['answer'])
    await state.clear()
    await msg.bot.send_message(msg.chat.id, 'Список типовых вопросов был обновлен!')
    await add_faq(msg)

async def delete_faq_callback(call: CallbackQuery) -> None:
    questions = db_manager.questions.get()
    if questions:
        keyboard = _build_faq_keyboard(questions)
        await call.message.bot.send_message(
            call.message.chat.id,
            text="Список вопросов, выберите который из них нужно удалить",
            reply_markup=keyboard
        )
    else:
        await call.message.bot.send_message(call.message.chat.id, 'Список пуст')

async def delete_question_callback(call: CallbackQuery) -> None:
    question_id = db_manager.questions.get()[int(call.data.split(':')[1]) - 1]['id']
    deleted = db_manager.questions.delete(question_id)
    questions = db_manager.questions.get()
    keyboard = _build_faq_keyboard(questions)
    await call.message.edit_text(call.message.text, reply_markup=keyboard)
    await call.message.bot.send_message(
        call.message.chat.id,
        'Список типовых вопросов был обновлен!' if deleted else 'Ошибка'
    )

async def exit_faq_callback(call: CallbackQuery) -> None:
    await call.message.delete()
    await call.message.bot.send_message(call.message.chat.id, 'Ок')

dp.callback_query.register(add_faq_callback, F.data.startswith('add_faq:click'))
dp.callback_query.register(delete_faq_callback, F.data.startswith('delete_faq:click'))
dp.callback_query.register(delete_question_callback, F.data.startswith('delete_question:'))
dp.callback_query.register(exit_faq_callback, F.data.startswith('exit:click'))