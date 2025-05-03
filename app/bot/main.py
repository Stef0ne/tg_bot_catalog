import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import SimpleEventIsolation

from app.bot.handlers.user_handler import user_private_router
from app.bot.handlers.group_handler import group_router
from app.db.engine import DatabaseMiddleware, sessionmanager
from app.bot.middlewares.access_middleware import AccessMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

API_TG_TOKEN = os.getenv('API_KEY_TG', None)
bot = Bot(token=API_TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(
    events_isolation=SimpleEventIsolation()
)

dp.update.middleware(DatabaseMiddleware())
dp.update.middleware(AccessMiddleware())

dp.include_routers(
    user_private_router,
    group_router
)

async def main():
 
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Starting polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logging.error(f"Error during polling: {e}", exc_info=True) 
    finally:
        logging.info("Closing database connection...")
        await sessionmanager.close()
        logging.info("Database connection closed.")


if __name__ == "__main__":
    try:
        logging.info("Init bot")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot failed: {e}", exc_info=True)