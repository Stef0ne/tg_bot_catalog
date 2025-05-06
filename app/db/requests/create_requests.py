import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category, Subcategory, ContentItem, User
from app.db.requests.get_requests import get_user_by_telegram_id


async def create_user(session: AsyncSession, telegram_id: int) -> User | None:
    existing_user = await get_user_by_telegram_id(session, telegram_id)
    if existing_user:
        return 
    new_user = User(telegram_id=telegram_id)
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except Exception as e:
        await session.rollback()
        raise logging.error("Ошибка в методе create_user", exc_info=e)

async def create_category(session: AsyncSession, name: str) -> Category | None:
    category = Category(name=name)
    try:
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category
    except Exception as e:
        await session.rollback()
        raise logging.error("Ошибка в методе create_category", exc_info=e)

async def create_subcategory(session: AsyncSession, name: str, category_id: int) -> Subcategory | None:
    subcategory = Subcategory(name=name, category_id=category_id)
    try:
        session.add(subcategory)
        await session.commit()
        await session.refresh(subcategory)
        return subcategory
    except Exception as e:
        await session.rollback()
        raise logging.error("Ошибка в методе create_subcategory", exc_info=e)

async def create_content_item(session: AsyncSession, text_content: str, subcategory_id: int) -> ContentItem | None:
    content_item = ContentItem(text_content=text_content, subcategory_id=subcategory_id)
    try:
        session.add(content_item)
        await session.commit()
        await session.refresh(content_item)
        return content_item
    except Exception as e:
        await session.rollback()
        raise logging.error("Ошибка в методе create_content_item", exc_info=e)
    
