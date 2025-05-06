from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category, Subcategory, User

async def delete_category(session: AsyncSession, category_id: int):
    query = delete(Category).where(Category.id == category_id)
    await session.execute(query)
    await session.commit()

async def delete_subcategory(session: AsyncSession, subcategory_id: int):
    query = delete(Subcategory).where(Subcategory.id == subcategory_id)
    await session.execute(query)
    await session.commit()

async def delete_user(session: AsyncSession, telegram_id: int):
    query = delete(User).where(User.telegram_id == telegram_id)
    await session.execute(query)
    await session.commit()
