from logging import info
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, F
from aiogram.filters import Command
from aiogram.types import TelegramObject

from database.connection import logs_db
from extra.create_bot import dp, bot
from modules.passive.on_start import on_start, sql_start


def on_start_bot() -> bool:
    if on_start() and sql_start():
        return True
    else:
        return False


class SomeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        info(f"User ID: {event.from_user.id} | Username: {event.from_user.username} | Message: {event.text}")
        logs_db().add(event.from_user.id,
                       event.from_user.username,
                       event.text,
                       event.date)
        result = await handler(event, data)
        return result


from modules.interaction import \
    add_faq, \
    admin_panel, \
    faq_window, \
    request_window, \
    scrolling_list, \
    show_answer_window, \
    start_window, \
    user_requests_window

# help_window, \


if __name__ == '__main__':
    on_start_bot()

    dp.message.register(add_faq.add_faq, Command('Типовые_вопросы(+/-)'))
    dp.message.register(add_faq.exit_state, add_faq.AddFaq.getting_faq, Command('Назад'))
    dp.message.register(add_faq.get_faq, add_faq.AddFaq.getting_faq)
    dp.message.register(add_faq.get_answer, add_faq.AddFaq.getting_answer)

    dp.message.register(admin_panel.admin_panel, Command('Админ'))

    dp.message.register(faq_window.faq_window, Command('Типовые_вопросы'))
    dp.message.register(faq_window.faq_question, faq_window.ChooseFaqWindow.faq_question)

    dp.message.register(request_window.request_window, Command('Подать_заявку'))
    dp.message.register(request_window.exit, request_window.RequestWindow.getting_message, Command('Выйти'))
    dp.message.register(request_window.get_photo, request_window.RequestWindow.getting_message, F.content_type.in_({"photo"}))
    dp.message.register(request_window.get_video, request_window.RequestWindow.getting_message, F.content_type.in_({"video"}))
    dp.message.register(request_window.response, request_window.RequestWindow.getting_message, F.content_type.in_({"text"}))

    dp.message.register(scrolling_list.list_cmd, Command("Вывод_заявок"))
    dp.message.register(scrolling_list.answer_message, scrolling_list.AnswerRequest.get_message)

    dp.message.register(show_answer_window.show_answer_window, Command('Показать'))
    dp.message.register(show_answer_window.hide_answer_window, Command('Не_показывать'))

    dp.message.register(start_window.start_window, Command('start', 'Назад'))

    dp.message.register(user_requests_window.user_requests_window, Command('Мои_заявки'))

    dp.message.middleware.register(SomeMiddleware())
    dp.run_polling(bot, skip_updates=True)