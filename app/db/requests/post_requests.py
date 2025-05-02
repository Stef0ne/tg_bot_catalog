from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.models import Category, Subcategory, ContentItem


async def create_category(session: AsyncSession, name: str) -> Category:
    category = Category(name=name)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

async def create_subcategory(session: AsyncSession, name: str, category_id: int) -> Subcategory:
    subcategory = Subcategory(name=name, category_id=category_id)
    session.add(subcategory)
    await session.commit()
    await session.refresh(subcategory)
    return subcategory

async def create_content_item(session: AsyncSession, text_content: str, subcategory_id: int) -> ContentItem:
    content_item = ContentItem(text_content=text_content, subcategory_id=subcategory_id)
    session.add(content_item)
    await session.commit()
    await session.refresh(content_item)
    return content_item
