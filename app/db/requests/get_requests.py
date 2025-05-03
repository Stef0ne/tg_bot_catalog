from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.models import Category, Subcategory, ContentItem, User


async def get_all_categories(session: AsyncSession) -> List[Category]:
    stmt = select(Category).order_by(Category.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_subcategories_by_category_id(category_id: int, session: AsyncSession) -> List[Subcategory]:
    stmt = select(Subcategory).where(Subcategory.category_id == category_id).order_by(Subcategory.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_content_item_by_subcategory_id(subcategory_id: int, session: AsyncSession) -> ContentItem:
    stmt = select(ContentItem).where(ContentItem.subcategory_id == subcategory_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_content_item_by_subcategory_id(
    session: AsyncSession,
    subcategory_id: int
) -> Optional[ContentItem]:
    stmt = select(ContentItem).where(ContentItem.subcategory_id == subcategory_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_category_by_id(
    session: AsyncSession,
    category_id: int
) -> Optional[Category]:
    category = await session.get(Category, category_id)
    return category

async def get_subcategory_by_id(
    session: AsyncSession,
    subcategory_id: int
) -> Optional[Subcategory]:
    subcategory = await session.get(Subcategory, subcategory_id)
    return subcategory

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> Optional[User]:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_all_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)