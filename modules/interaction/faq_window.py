from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from modules.interaction.start_window import start_window
from database.connection import questions_db
from modules.interaction.keyboards.keyboards_list import Keyboard


class ChooseFaqWindow(StatesGroup):
    faq_question = State()


async def faq_window(msg: types.Message, state: FSMContext) -> None:
    questions = questions_db().get()
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb2)
    await msg.bot.send_message(msg.from_user.id,
                               """В данном разделе представлены часто задаваемые вопросы.\n{}\nВам помог этот раздел?""".format('\n'.join(list(f"{i} - {questions[i - 1]['question']}: {questions[i - 1]['answer']}" for i in range(1, len(questions)+1)))) if len(questions) > 0 else "Тут ничего нет",
                               reply_markup=keyboard if len(questions) > 0 else None)
    await state.set_state(ChooseFaqWindow.faq_question) if len(questions) > 0 else None


async def faq_question(msg: types.Message, state: FSMContext) -> None:
    if msg.text.startswith('Да'):
        await state.clear()
        await msg.bot.send_message(msg.chat.id, "Рад,что смог Вам помочь.")
        await start_window(msg)
    elif msg.text.startswith('Нет'):
        keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb4)
        await msg.bot.send_message(msg.chat.id, "Вы можете отправить Ваш запрос в разделе <Подать заявку>.", reply_markup=keyboard)
        await state.clear()