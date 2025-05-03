from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.callbacks.menu_callback import AdminUserCallbackData, AdminSectionCallbackData, AdminMenuCallbackData
from app.db.requests.get_requests import (
    get_all_categories,
    get_subcategories_by_category_id,
    get_content_item_by_subcategory_id
)

# Константы для уровней меню
LEVEL_CATEGORIES = 0
LEVEL_SUBCATEGORIES = 1
LEVEL_CONTENT = 2


def get_main_manage_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Управление пользователями", 
        callback_data=AdminUserCallbackData(
            action="manage"
        )
    )
    builder.button(
        text="Управление разделами", 
        callback_data=AdminSectionCallbackData(
            action="manage"
        )
    ) 
    builder.adjust(1)
    return builder.as_markup()

def get_user_management_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Список пользователей", 
        callback_data=AdminUserCallbackData(
            category="users",
            action="list"
        )
    )
    builder.button(
        text="Добавить пользователя", 
        callback_data=AdminUserCallbackData(
            category="users",
            action="add_user"
        )
    )
    builder.button(
        text="Удалить пользователя", 
        callback_data=AdminUserCallbackData(
            category="users",
            action="delete_user"
        )
    )
    builder.button(
        text="Назад",
        callback_data=AdminUserCallbackData(
            action="back"
        )
    )
    builder.adjust(1)
    return builder.as_markup()

async def get_section_management_keyboard(session: AsyncSession) -> InlineKeyboardMarkup:
    categories = await get_all_categories(session=session)
    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(
            text=category.name,
            callback_data=AdminMenuCallbackData(
                level=LEVEL_CATEGORIES,
                category_id=category.id
            )
        )
    builder.button(
        text="Добавить раздел",
        callback_data=AdminSectionCallbackData(
            action="add_category"
        )
    )
    builder.button(
        text="Назад",
        callback_data=AdminSectionCallbackData(
            action="back"
        )
    )
    builder.adjust(1)
    return builder.as_markup()

async def get_subcategory_management_keyboard(category_id: int, session: AsyncSession) -> InlineKeyboardMarkup:
    subcategories = await get_subcategories_by_category_id(category_id=category_id, session=session)
    builder = InlineKeyboardBuilder()
    if subcategories:
        for subcategory in subcategories:
            builder.button(
                text=subcategory.name,
                callback_data=AdminMenuCallbackData(
                    level=LEVEL_SUBCATEGORIES,
                    category_id=category_id,
                    subcategory_id=subcategory.id
                )
            )
    builder.button(
        text="Добавить подраздел",
        callback_data=AdminSectionCallbackData(
            action="add_subcategory",
            category_id=category_id 
        )
    )
    builder.button(
        text="Редактировать раздел",
        callback_data=AdminSectionCallbackData(
            action="edit_category",
            category_id=category_id 
        )
    )
    builder.button(
        text="Удалить раздел",
        callback_data=AdminSectionCallbackData(
            action="delete_category",
            category_id=category_id 
        )
    )
    builder.button(
        text="Назад",
        callback_data=AdminSectionCallbackData(
            action="manage"
        )
    )
    builder.adjust(1)
    return builder.as_markup()

async def get_content_management_keyboard(subcategory_id: int, session: AsyncSession) -> InlineKeyboardMarkup:
    content_item = await get_content_item_by_subcategory_id(
        session=session,
        subcategory_id=subcategory_id
    )
    builder = InlineKeyboardBuilder()
    if content_item:
        builder.button(
            text="Редактировать контент",
            callback_data=AdminSectionCallbackData(
                action="edit_content_item",
                subcategory_id=subcategory_id
            )
        )
    else:
        builder.button(
            text="Добавить контент",
            callback_data=AdminSectionCallbackData(
                action="add_content_item",
                subcategory_id=subcategory_id
            )
        )
    builder.button(
        text="Редактировать подраздел",
        callback_data=AdminSectionCallbackData(
            action="edit_subcategory",
            subcategory_id=subcategory_id
        )
    )
    builder.button(
        text="Удалить подраздел",
        callback_data=AdminSectionCallbackData(
            action="delete_subcategory",
            subcategory_id=subcategory_id
        )
    )
    builder.button(
        text="Назад",
        callback_data=AdminSectionCallbackData(
            action="back_subcategory"
        )
    )
    builder.adjust(1)
    return builder.as_markup()
        

def get_cancel_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отмена", 
        callback_data=AdminSectionCallbackData(
            action="manage"
        )
    )
    return builder.as_markup()

def get_cancel_button_fsm() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отмена",
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    )
    return builder.as_markup()

def get_add_section_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Создать", 
        callback_data=AdminSectionCallbackData(
            action="confirm_add_category"
        )
    )
    builder.button(
        text="Отмена",
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def get_edit_section_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сохранить", 
        callback_data=AdminSectionCallbackData(
            action="confirm_edit_category"
        )
    )
    builder.button(
        text="Отмена", 
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    ) 
    builder.adjust(2)
    return builder.as_markup()

def get_delete_section_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Удалить",
        callback_data=AdminSectionCallbackData(
            action="confirm_delete_category"
        )
    )
    builder.button(
        text="Отмена",
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    )
    return builder.as_markup()

def get_add_subsection_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Создать", 
        callback_data=AdminSectionCallbackData(
            action="confirm_add_subcategory"
        )
    )
    builder.button(
        text="Отмена",
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def get_edit_subsection_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сохранить", 
        callback_data=AdminSectionCallbackData(
            action="confirm_edit_subcategory"
        )
    )
    builder.button(
        text="Отмена", 
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    ) 
    builder.adjust(2)
    return builder.as_markup()

def get_delete_subsection_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Удалить",
        callback_data=AdminSectionCallbackData(
            action="confirm_delete_subcategory"
        )
    )
    builder.button(
        text="Отмена",
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    )
    return builder.as_markup()

def get_add_content_item_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Создать", 
        callback_data=AdminSectionCallbackData(
            action="confirm_add_content_item"
        )
    )
    builder.button(
        text="Отмена",
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def get_edit_content_item_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сохранить", 
        callback_data=AdminSectionCallbackData(
            action="confirm_edit_content_item"
        )
    )
    builder.button(
        text="Отмена", 
        callback_data=AdminSectionCallbackData(
            action="cancel_fsm"
        )
    ) 
    builder.adjust(2)
    return builder.as_markup()

def get_cancel_button_for_users() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отмена",
        callback_data=AdminUserCallbackData(
            action="manage"
        )
    )
    return builder.as_markup()