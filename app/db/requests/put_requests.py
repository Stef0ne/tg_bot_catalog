from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category, Subcategory, ContentItem

# назвать файл лучше не put а update 

# не плохо возвращать объект обновления 

async def update_category_name(session: AsyncSession, category_id: int, new_name: str) -> None:
    stmt = (
        update(Category)
        .where(Category.id == category_id)
        .values(name=new_name)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt) 
    await session.commit()
    
async def update_subcategory_name(session: AsyncSession, subcategory_id: int, new_name: str) -> None:
    stmt = (
        update(Subcategory)
        .where(Subcategory.id == subcategory_id)
        .values(name=new_name)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt) 
    await session.commit()

async def update_content_item_text(session: AsyncSession, subcategory_id: int, text_content: str) -> None:
    stmt = (
        update(ContentItem)
        .where(ContentItem.subcategory_id == subcategory_id)
        .values(text_content=text_content)
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt) 
    await session.commit()

