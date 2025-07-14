from dataclasses import dataclass
from aiogram.types import KeyboardButton


@dataclass
class Keyboard:
    """ Keyboard dataclass """
    kb1 = [[KeyboardButton(text="/Типовые_вопросы")],
           [KeyboardButton(text="/Подать_заявку")],
           [KeyboardButton(text="/Мои_заявки")]]

    kb2 = [[KeyboardButton(text="Да")],
           [KeyboardButton(text="Нет")],
           [KeyboardButton(text="/Назад")]]

    kb_answer = [[KeyboardButton(text="/Показать")],
                 [KeyboardButton(text="/Не_показывать")]]

    kb3 = [[KeyboardButton(text="/Выйти")]]

    kb4 = [[KeyboardButton(text="/Назад")],
           [KeyboardButton(text="/Подать_заявку")]]

    kb_admin = [[KeyboardButton(text="/Типовые_вопросы")],
                [KeyboardButton(text="/Подать_заявку")],
                [KeyboardButton(text="/Мои_заявки")],
                [KeyboardButton(text="/Админ")]]

    kb_admin_panel = [[KeyboardButton(text="/Вывод_заявок")],
                      [KeyboardButton(text="/Типовые_вопросы(+/-)")],
                      [KeyboardButton(text="/Назад")]]
