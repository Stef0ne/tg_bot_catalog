from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.models import Category, Subcategory, ContentItem
from app.bot.callbacks.menu_callback import MenuCallbackData

# Константы для уровней меню
LEVEL_CATEGORIES = 0
LEVEL_SUBCATEGORIES = 1
LEVEL_CONTENT = 2

async def build_main_menu_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    """Строит клавиатуру для главного меню (список категорий)."""
    stmt = select(Category).order_by(Category.id)
    result = await session.execute(stmt)
    categories = result.scalars().all()

    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=category.name,
            callback_data=MenuCallbackData(
                level=LEVEL_CATEGORIES,
                category_id=category.id
            )
        )
    builder.adjust(1)
    return builder.as_markup()


async def build_submenu_keyboard(category_id: int, session: AsyncSession) -> InlineKeyboardMarkup:
    """Строит клавиатуру для подменю (список подкатегорий)."""
    stmt = (
        select(Subcategory)
        .where(Subcategory.category_id == category_id)
        .order_by(Subcategory.id)
    )
    result = await session.execute(stmt)
    subcategories = result.scalars().all()

    builder = InlineKeyboardBuilder()
    if not subcategories:
        return builder.as_markup()
        
    for subcategory in subcategories:
        builder.button(
            text=subcategory.name,
            callback_data=MenuCallbackData(
                level=LEVEL_SUBCATEGORIES,
                category_id=category_id,
                subcategory_id=subcategory.id
            )
        )

    builder.adjust(1)
    return builder.as_markup()