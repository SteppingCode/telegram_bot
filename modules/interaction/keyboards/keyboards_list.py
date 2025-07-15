from dataclasses import dataclass
from aiogram.types import KeyboardButton
from typing import List, ClassVar

# Define buttons and layouts at the module level
_buttons = {
    "faq": KeyboardButton(text="/faq"),
    "submit_request": KeyboardButton(text="/submit_request"),
    "my_requests": KeyboardButton(text="/my_requests"),
    "back": KeyboardButton(text="/back"),
    "yes": KeyboardButton(text="Да"),
    "no": KeyboardButton(text="Нет"),
    "show": KeyboardButton(text="/show"),
    "hide": KeyboardButton(text="/hide"),
    "exit": KeyboardButton(text="/exit"),
    "admin": KeyboardButton(text="/admin"),
    "list_requests": KeyboardButton(text="/list_requests"),
    "add_faq": KeyboardButton(text="/add_faq"),
}

_layouts = {
    "kb1": [["faq"], ["submit_request"], ["my_requests"]],
    "kb2": [["yes"], ["no"], ["back"]],
    "kb_answer": [["show"], ["hide"]],
    "kb3": [["exit"]],
    "kb4": [["back"], ["submit_request"]],
    "kb_admin": [["faq"], ["submit_request"], ["my_requests"], ["admin"]],
    "kb_admin_panel": [["list_requests"], ["add_faq"], ["back"]],
}

# Compute keyboard layouts outside the class
kb1 = [[_buttons[button_key] for button_key in row] for row in _layouts["kb1"]]
kb2 = [[_buttons[button_key] for button_key in row] for row in _layouts["kb2"]]
kb_answer = [[_buttons[button_key] for button_key in row] for row in _layouts["kb_answer"]]
kb3 = [[_buttons[button_key] for button_key in row] for row in _layouts["kb3"]]
kb4 = [[_buttons[button_key] for button_key in row] for row in _layouts["kb4"]]
kb_admin = [[_buttons[button_key] for button_key in row] for row in _layouts["kb_admin"]]
kb_admin_panel = [[_buttons[button_key] for button_key in row] for row in _layouts["kb_admin_panel"]]

@dataclass
class Keyboard:
    kb1: ClassVar[List[List[KeyboardButton]]] = kb1
    kb2: ClassVar[List[List[KeyboardButton]]] = kb2
    kb_answer: ClassVar[List[List[KeyboardButton]]] = kb_answer
    kb3: ClassVar[List[List[KeyboardButton]]] = kb3
    kb4: ClassVar[List[List[KeyboardButton]]] = kb4
    kb_admin: ClassVar[List[List[KeyboardButton]]] = kb_admin
    kb_admin_panel: ClassVar[List[List[KeyboardButton]]] = kb_admin_panel