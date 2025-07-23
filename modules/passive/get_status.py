from aiogram import types

from extra.config import Data


async def is_admin(msg: types.Message) -> bool:
    status = await msg.bot.get_chat_member(chat_id=Data.group_id, user_id=msg.from_user.id)
    if type(status) is not types.chat_member_left.ChatMemberLeft:
        return True
    else:
        return False
