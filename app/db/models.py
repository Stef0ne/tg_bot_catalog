from typing import List, Optional

from sqlalchemy import String, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.engine import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    subcategories: Mapped[List["Subcategory"]] = relationship(
        back_populates="category",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Subcategory(Base):
    __tablename__ = 'subcategories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='CASCADE'), 
        nullable=False, 
        index=True
    )

    category: Mapped["Category"] = relationship(
        back_populates="subcategories",
        lazy="joined"
    )

    content_item: Mapped[Optional["ContentItem"]] = relationship(
        back_populates="subcategory",
        uselist=False,
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Subcategory(id={self.id}, name='{self.name}', category_id={self.category_id})>"


class ContentItem(Base):
    __tablename__ = 'content_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    subcategory_id: Mapped[int] = mapped_column(
        ForeignKey('subcategories.id', ondelete='CASCADE'),
        nullable=False,
        unique=True,
        index=True
    )

    subcategory: Mapped["Subcategory"] = relationship(
        back_populates="content_item",
        lazy="joined"
    )

    def __repr__(self):
        return f"<ContentItem(id={self.id}, subcategory_id={self.subcategory_id})>" 
    

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"