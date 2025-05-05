from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category, Subcategory, ContentItem, User

# везде первым аргументом лучше передавать сессию
async def get_all_categories(session: AsyncSession) -> list[Category]:
    stmt = select(Category).order_by(Category.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_subcategories_by_category_id(session: AsyncSession, category_id: int) -> list[Subcategory]:
    stmt = select(Subcategory).where(Subcategory.category_id == category_id).order_by(Subcategory.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_content_item_by_subcategory_id(
    session: AsyncSession,
    subcategory_id: int
) -> ContentItem | None:
    stmt = select(ContentItem).where(ContentItem.subcategory_id == subcategory_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_category_by_id(
    session: AsyncSession,
    category_id: int
) -> Category | None:
    category = await session.get(Category, category_id)
    return category

async def get_subcategory_by_id(
    session: AsyncSession,
    subcategory_id: int
) -> Subcategory | None:
    subcategory = await session.get(Subcategory, subcategory_id)
    return subcategory

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_all_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users) # зачем лист?