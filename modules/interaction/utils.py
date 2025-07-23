from typing import Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


async def send_media_if_exists(bot, chat_id, request_data) -> None:
    if 'photo_id' in request_data and request_data['photo_id']:
        await bot.send_photo(chat_id, request_data['photo_id'])
    if 'video_id' in request_data and request_data['video_id']:
        await bot.send_video(chat_id, request_data['video_id'])


async def obscene_check(template: str, chain_input: dict[str:Any]) -> bool:
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_template(template)
    model: OllamaLLM = OllamaLLM(model="gemma3n:e2b")
    chain = prompt | model
    res: str = chain.invoke(chain_input)
    return bool(int(res))
