from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category, Subcategory

# я бы сделал сначала get объекта, если его нет 
# выкидывать кастомную ошибку, а потом этот оbj 
# передавал в session.delete(obj) и делал return obj
# если все ок
async def delete_category(session: AsyncSession, category_id: int):
    query = delete(Category).where(Category.id == category_id)
    await session.execute(query)
    await session.commit()

async def delete_subcategory(session: AsyncSession, subcategory_id: int):
    query = delete(Subcategory).where(Subcategory.id == subcategory_id)
    await session.execute(query)
    await session.commit()

