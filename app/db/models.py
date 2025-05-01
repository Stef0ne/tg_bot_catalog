from sqlalchemy import Column, Integer, String, SmallInteger, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, declared_attr

from app.db.engine import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    subcategories = relationship("Subcategory", back_populates="category", lazy="selectin")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class Subcategory(Base):
    __tablename__ = 'subcategories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False) 
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False, index=True) 

    category = relationship("Category", back_populates="subcategories", lazy="joined")

    content_item = relationship("ContentItem", back_populates="subcategory", uselist=False, lazy="selectin")

    def __repr__(self):
        return f"<Subcategory(id={self.id}, name='{self.name}', category_id={self.category_id})>"


class ContentItem(Base):
    __tablename__ = 'content_items'

    id = Column(Integer, primary_key=True)
    text_content = Column(Text, nullable=False)

    subcategory_id = Column(Integer, ForeignKey('subcategories.id'), nullable=False, unique=True, index=True)

    subcategory = relationship("Subcategory", back_populates="content_item", lazy="joined")

    def __repr__(self):
        return f"<ContentItem(id={self.id}, subcategory_id={self.subcategory_id})>" 