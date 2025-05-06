import logging

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as AiogramUser 
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.requests.get_requests import get_user_by_telegram_id
from app.db.models import User as DBUser


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Awaitable[Any]:
        aiogram_user: AiogramUser | None = data.get('event_from_user', None)
        session: AsyncSession | None = data.get('db_session')
        
        if not aiogram_user:
            return await handler(event, data)

        if not session:
             logging.error("DB Session not found in data for AccessMiddleware")
             return 
         
        user_id = aiogram_user.id
        db_user = await get_user_by_telegram_id(session, user_id)

        if db_user:
            needs_update = False
            if db_user.username != aiogram_user.username:
                db_user.username = aiogram_user.username
                needs_update = True
            if db_user.first_name != aiogram_user.first_name:
                db_user.first_name = aiogram_user.first_name
                needs_update = True
            if needs_update:
                try:
                    session.add(db_user) 
                    await session.commit()
                    await session.refresh(db_user) 
                    logging.info(f"User data updated for user_id: {user_id}")
                except Exception as e:
                    await session.rollback()
                    logging.error(f"Failed to update user data for user_id: {user_id} - {e}")

            data['db_user'] = db_user
            return await handler(event, data) 
        else:
            logging.info(f"Access denied for non-registered user: {user_id}")
            # Можно отправить сообщение пользователю перед отменой (для CallbackQuery лучше answer)
            # if isinstance(event, types.CallbackQuery):
            #     try:
            #         await event.answer("У вас нет доступа.", show_alert=True)
            #     except Exception as e:
            #         logging.error(f"Failed to answer callback for denied user {user_id}: {e}")
            # elif isinstance(event, types.Message):
            #     try:
            #         await event.answer("У вас нет доступа к этому боту.")
            #     except Exception as e:
            #         logging.error(f"Failed to answer message for denied user {user_id}: {e}")
            # Просто прекращаем обработку, не вызывая следующий хэндлер
            return 