from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.requests.get_requests import (
    get_all_categories,
    get_subcategories_by_category_id,
)
from app.bot.callbacks.menu_callback import UserMenuCallbackData

# Константы для уровней меню
LEVEL_CATEGORIES = 0
LEVEL_SUBCATEGORIES = 1
LEVEL_CONTENT = 2

async def build_main_menu_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    categories = await get_all_categories(session=session)

    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=category.name,
            callback_data=UserMenuCallbackData(
                level=LEVEL_CATEGORIES,
                category_id=category.id
            )
        )
    builder.adjust(1)
    return builder.as_markup()


async def build_submenu_keyboard(category_id: int, session: AsyncSession) -> InlineKeyboardMarkup:
    subcategories = await get_subcategories_by_category_id(category_id=category_id, session=session)

    builder = InlineKeyboardBuilder()
    if not subcategories:
        return builder.as_markup()
        
    for subcategory in subcategories:
        builder.button(
            text=subcategory.name,
            callback_data=UserMenuCallbackData(
                level=LEVEL_SUBCATEGORIES,
                category_id=category_id,
                subcategory_id=subcategory.id
            )
        )

    builder.adjust(1)
    return builder.as_markup()