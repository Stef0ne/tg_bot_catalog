from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.bot.callbacks.menu_callback import AdminUserCallbackData, AdminSectionCallbackData


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
            action="add"
        )
    )
    builder.button(
        text="Удалить пользователя", 
        callback_data=AdminUserCallbackData(
            category="users",
            action="delete"
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

def get_section_management_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Раздел 1",
        callback_data=AdminSectionCallbackData(
            action="section_1"
        )
    )
    builder.button(
        text="Раздел 2",
        callback_data=AdminSectionCallbackData(
            action="section_2"
        )
    )
    builder.button(
        text="Добавить раздел",
        callback_data=AdminSectionCallbackData(
            action="add"
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

def get_cancel_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отмена", 
        callback_data=AdminUserCallbackData(
            action="manage"
        )
    )
    return builder.as_markup()