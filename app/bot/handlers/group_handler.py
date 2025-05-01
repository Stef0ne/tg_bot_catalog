import logging
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.keyboard_admin import (
    get_main_manage_keyboard, 
    get_user_management_keyboard,
    get_section_management_keyboard,
    get_cancel_button
)
from app.bot.callbacks.menu_callback import AdminUserCallbackData, AdminSectionCallbackData

GROUP_ID = -4695868814

group_router = Router()
group_router.message.filter(F.chat.id == GROUP_ID)
group_router.callback_query.filter(F.message.chat.id == GROUP_ID)

@group_router.message(Command("chat_id"))
async def get_chat_id_command(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"ID этого чата: `{chat_id}`")

@group_router.message(Command("admin"))
async def cmd_manage_in_group(message: types.Message):
    await message.answer(
        "Меню управления:",
        reply_markup=get_main_manage_keyboard()
    )

@group_router.callback_query(AdminUserCallbackData.filter(F.action == "manage"))
async def show_user_management_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Управление пользователями:", reply_markup=get_user_management_keyboard())
    await callback.answer()

@group_router.callback_query(AdminUserCallbackData.filter(F.action == "list"))
async def handle_users_list(callback: types.CallbackQuery):
    users_text = "Список пользователей (заглушка):\n- User1\n- User2"
    await callback.message.edit_text(users_text, reply_markup=get_user_management_keyboard()) 
    await callback.answer()

@group_router.callback_query(AdminUserCallbackData.filter(F.action == "add"))
async def handle_users_add_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Запуск добавления пользователя (заглушка)... Напишите ID.", 
        reply_markup=get_cancel_button()
    )
    await callback.answer()

@group_router.callback_query(AdminUserCallbackData.filter(F.action == "delete"))
async def handle_users_delete_start(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Запуск удаления пользователя (заглушка)... Напишите Username.", 
        reply_markup=get_cancel_button()
    )
    await callback.answer()
    
@group_router.callback_query(AdminUserCallbackData.filter(F.action == "back"))
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "back"))
async def handle_back_to_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_manage_keyboard()
    )
    await callback.answer()
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "manage"))
async def show_section_management_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите раздел для редактирования или добавьте новый:",
        reply_markup=get_section_management_keyboard()
    )
    await callback.answer()
    

