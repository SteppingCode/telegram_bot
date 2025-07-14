from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from extra.config import Data

# from aiogram.client.session.aiohttp import AiohttpSession

# session = AiohttpSession(proxy="http://proxy.server:3128/")

bot: Bot = Bot(token=Data.token)  # , session=session)
dp: Dispatcher = Dispatcher(Bot=bot, storage=MemoryStorage())
