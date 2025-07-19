from logging import info
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, F
from aiogram.filters import Command
from aiogram.types import TelegramObject

from database.connection import db_manager
from extra.create_bot import dp, bot
from modules.passive.on_start import on_start, sql_start

from modules.interaction import (
    add_faq,
    admin_panel,
    faq_window,
    request_window,
    scrolling_list,
    show_answer_window,
    start_window,
    user_requests_window
)

class SomeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            _handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        info(f"User ID: {event.from_user.id} | Username: {event.from_user.username} | Message: {event.text}")
        db_manager.logs.add(event.from_user.id,
                            event.from_user.username,
                            event.text,
                            event.date)
        result = await _handler(event, data)
        return result

COMMAND_HANDLERS = [
    {
        "handler": add_faq.add_faq,
        "commands": ["add_faq"]
    },
    {
        "handler": add_faq.exit_state,
        "state": add_faq.AddFaq.getting_faq,
        "commands": ["back"]
    },
    {
        "handler": add_faq.get_faq,
        "state": add_faq.AddFaq.getting_faq
    },
    {
        "handler": add_faq.get_answer,
        "state": add_faq.AddFaq.getting_answer
    },
    {
        "handler": admin_panel.admin_panel,
        "commands": ["admin"]
    },
    {
        "handler": faq_window.faq_window,
        "commands": ["faq"]
    },
    {
        "handler": faq_window.faq_question,
        "state": faq_window.ChooseFaqWindow.faq_question
    },
    {
        "handler": request_window.request_window,
        "commands": ["submit_request"]
    },
    {
        "handler": request_window.exit_state,
        "state": request_window.RequestWindow.getting_message,
        "commands": ["exit"]
    },
    {
        "handler": request_window.get_photo,
        "state": request_window.RequestWindow.getting_message,
        "filters": F.content_type.in_({"photo"})
    },
    {
        "handler": request_window.get_video,
        "state": request_window.RequestWindow.getting_message,
        "filters": F.content_type.in_({"video"})
    },
    {
        "handler": request_window.response,
        "state": request_window.RequestWindow.getting_message,
        "filters": F.content_type.in_({"text"})
    },
    {
        "handler": scrolling_list.list_cmd,
        "commands": ["list_requests"]
    },
    {
        "handler": scrolling_list.answer_message,
        "state": scrolling_list.AnswerRequest.get_message
    },
    {
        "handler": show_answer_window.show_answer_window,
        "commands": ["show"]
    },
    {
        "handler": show_answer_window.hide_answer_window,
        "commands": ["hide"]
    },
    {
        "handler": start_window.start_window,
        "commands": ["start", "back"]
    },
    {
        "handler": user_requests_window.user_requests_window,
        "commands": ["my_requests"]
    }
]

if __name__ == "__main__":
    if not (on_start() and sql_start()):
        raise RuntimeError("Failed to initialize bot or database")

    for i, handler_config in enumerate(COMMAND_HANDLERS):
        handler = handler_config["handler"]
        commands = handler_config.get("commands")
        state = handler_config.get("state")
        filters = handler_config.get("filters")

        if handler is None or not callable(handler):
            info(f"Skipping invalid handler {i+1}: {handler_config}")
            continue

        try:
            if commands:
                dp.message.register(handler, Command(*commands))
            elif filters:
                dp.message.register(handler, filters, state)
            else:
                dp.message.register(handler, state)
            info(f"Successfully registered handler {i+1}")
        except Exception as e:
            info(f"Error registering handler {i+1}: {e}")

    dp.message.middleware.register(SomeMiddleware())
    dp.run_polling(bot, skip_updates=True)