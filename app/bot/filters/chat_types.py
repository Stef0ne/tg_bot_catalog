from typing import List

from aiogram import types
from aiogram.filters import Filter

class ChatTypeFilter(Filter):
    def __init__(self, chat_types: List[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message | types.CallbackQuery) -> bool:
        # Проверяем тип события и получаем чат
        if isinstance(message, types.Message):
            chat = message.chat
        elif isinstance(message, types.CallbackQuery) and message.message:
            chat = message.message.chat
        else:
            return False
        return chat.type in self.chat_types