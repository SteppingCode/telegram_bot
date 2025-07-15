from datetime import datetime
from aiogram import types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from typing import List, Dict, Optional

from modules.interaction.keyboards.keyboards_list import Keyboard
from modules.passive.get_status import is_admin
from database.connection import db_manager
from extra.create_bot import dp

class AnswerRequest(StatesGroup):
    get_message = State()

class RequestPaginator:
    """Helper class to manage pagination and keyboard creation for requests."""
    ITEMS_PER_PAGE = 5

    def __init__(self):
        self.current_page = 1
        self.max_pages = 1

    def _get_unanswered_requests(self) -> List[Dict]:
        """Fetch unanswered requests from the database."""
        data = db_manager.requests.get()
        return [req for req in data if len(req['answer']) == 0]

    def _calculate_pagination(self, requests: List[Dict]) -> None:
        """Calculate max pages based on request count."""
        self.max_pages = (len(requests) // self.ITEMS_PER_PAGE) + (1 if len(requests) % self.ITEMS_PER_PAGE else 0) or 1

    def _build_request_buttons(self, requests: List[Dict], current_id: Optional[int] = None) -> List[tuple[str, str]]:
        """Build buttons for the current page of requests."""
        start_idx = self.ITEMS_PER_PAGE * (self.current_page - 1)
        end_idx = min(self.ITEMS_PER_PAGE * self.current_page, len(requests))
        buttons = []
        for i, req in enumerate(requests[start_idx:end_idx], start_idx + 1):
            text = f"{i:=^{len(str(i)) + 12}}" if current_id == req['id'] else f"{i} - {req['message']}"
            buttons.append((text, f"info:{req['id']}"))
        return buttons

    def build_keyboard(self, requests: List[Dict], current_id: Optional[int] = None, include_actions: bool = False) -> types.InlineKeyboardMarkup:
        """Build an inline keyboard for the request list with optional navigation and action buttons."""
        keyboard = InlineKeyboardBuilder()
        # Add request buttons
        for text, callback_data in self._build_request_buttons(requests, current_id):
            keyboard.button(text=text, callback_data=callback_data)
        # Add navigation and exit buttons
        buttons = []
        if self.current_page > 1:
            buttons.append(("←", "previous:click"))
        buttons.append((f"{self.current_page}/{self.max_pages}", "current_page:click"))
        if self.current_page < self.max_pages:
            buttons.append(("→", "next:click"))
        if include_actions and current_id:
            buttons.extend([
                ("Удалить", f"delete:{current_id}"),
                ("Ответить", f"answer:{current_id}")
            ])
        buttons.append(("Выйти", "exit:click"))
        for text, callback_data in buttons:
            keyboard.button(text=text, callback_data=callback_data)
        # Adjust layout dynamically
        request_count = min(self.ITEMS_PER_PAGE, len(requests) - self.ITEMS_PER_PAGE * (self.current_page - 1))
        adjust = [1] * request_count + ([3] if 1 < self.current_page < self.max_pages else [2]) + ([2] if include_actions else [1])
        keyboard.adjust(*adjust)
        return keyboard.as_markup()

    async def list_requests(self, msg: types.Message) -> List[Dict]:
        """Fetch requests and update pagination state."""
        requests = self._get_unanswered_requests()
        self._calculate_pagination(requests)
        self.current_page = 1
        return requests

    def update_page(self, direction: str) -> None:
        """Update the current page for navigation."""
        if direction == "next" and self.current_page < self.max_pages:
            self.current_page += 1
        elif direction == "previous" and self.current_page > 1:
            self.current_page -= 1

# Singleton paginator instance
paginator = RequestPaginator()

async def list_cmd(msg: types.Message, state: FSMContext = None) -> None:
    if not await is_admin(msg):
        await msg.bot.send_message(msg.chat.id, 'Вы не сотрудник БМЗ!')
        return
    requests = await paginator.list_requests(msg)
    text = 'Список' if requests else 'У вас нету заявок'
    keyboard = paginator.build_keyboard(requests) if requests else InlineKeyboardBuilder().button(text="У вас нету заявок", callback_data="requests:empty").adjust(1).as_markup()
    await msg.bot.send_message(chat_id=msg.chat.id, text=text, reply_markup=keyboard)

async def response(call: CallbackQuery) -> None:
    requests = paginator._get_unanswered_requests()
    request_id = int(call.data.split(':')[1])
    single_request = db_manager.requests.get(request_id)
    keyboard = paginator.build_keyboard(requests, current_id=request_id, include_actions=True)
    text = (f"ID: {single_request[0]}\n"
            f"Message: {single_request[3]}\n"
            f"Time: {single_request[6]}\n"
            f"{'Answer: ' + single_request[7] + '\nAnswer Time: ' + single_request[8] if single_request[7] else 'No answer':=^21}")
    await call.message.edit_text(text=text, reply_markup=keyboard)
    if single_request[4]:
        await call.message.bot.send_photo(call.message.chat.id, single_request[4])
    if single_request[5]:
        await call.message.bot.send_video(call.message.chat.id, single_request[5])
    if single_request[3] and (single_request[4] or single_request[5]):
        await call.message.bot.send_message(call.message.chat.id, f"{single_request[3]} : {single_request[6]}")

async def next_click(call: CallbackQuery) -> None:
    requests = paginator._get_unanswered_requests()
    paginator.update_page("next")
    keyboard = paginator.build_keyboard(requests) if requests else InlineKeyboardBuilder().button(text="У вас нету заявок", callback_data="requests:empty").adjust(1).as_markup()
    await call.message.edit_text(text=call.message.text, reply_markup=keyboard)

async def previous_click(call: CallbackQuery) -> None:
    requests = paginator._get_unanswered_requests()
    paginator.update_page("previous")
    keyboard = paginator.build_keyboard(requests) if requests else InlineKeyboardBuilder().button(text="У вас нету заявок", callback_data="requests:empty").adjust(1).as_markup()
    await call.message.edit_text(text=call.message.text, reply_markup=keyboard)

async def delete_request(call: CallbackQuery) -> None:
    request_id = int(call.data.split(":")[1])
    db_manager.requests.delete(request_id)
    requests = paginator._get_unanswered_requests()
    paginator._calculate_pagination(requests)
    if paginator.current_page > paginator.max_pages:
        paginator.current_page = paginator.max_pages
    keyboard = paginator.build_keyboard(requests) if requests else InlineKeyboardBuilder().button(text="У вас нету заявок", callback_data="requests:empty").adjust(1).as_markup()
    await call.message.edit_text(text='Список', reply_markup=keyboard)

async def answer_handler(call: CallbackQuery, state: FSMContext) -> None:
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_admin_panel)
    request_id = int(call.data.split(':')[1])
    await state.update_data(request_id=request_id)
    await call.message.bot.send_message(call.message.chat.id, "Напишите ответ на сообщение", reply_markup=keyboard)
    await state.set_state(AnswerRequest.get_message)

async def exit_state(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.bot.send_message(call.message.chat.id, "Ок")

async def answer_message(msg: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    request_id = data['request_id']
    now = datetime.now()
    request = db_manager.requests.get(request_id)
    db_manager.requests.update(request_id, msg.text, f"{now:%y.%m.%d (%H:%M)}")
    keyboard = types.ReplyKeyboardMarkup(keyboard=Keyboard.kb_answer)
    await msg.bot.send_message(msg.chat.id, "Ваш ответ добавлен")
    await msg.bot.send_message(request[1], "Вам ответили на сообщение", reply_markup=keyboard)
    await state.clear()

async def exit_callback(call: CallbackQuery) -> None:
    await call.message.delete()

dp.callback_query.register(response, F.data.startswith('info:'))
dp.callback_query.register(next_click, F.data.startswith('next:click'))
dp.callback_query.register(previous_click, F.data.startswith('previous:click'))
dp.callback_query.register(delete_request, F.data.startswith("delete:"))
dp.callback_query.register(answer_handler, F.data.startswith('answer:'))
dp.callback_query.register(exit_state, AnswerRequest.get_message, Command('Назад'))
dp.callback_query.register(exit_callback, F.data.startswith("exit:click"))