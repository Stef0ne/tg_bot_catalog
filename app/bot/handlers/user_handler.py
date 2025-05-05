import logging

from typing import Dict, Optional

from aiogram import F, Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.callbacks.menu_callback import UserMenuCallbackData
from app.bot.keyboards.keyboard_builder import (
    build_main_menu_keyboard,
    build_submenu_keyboard,
    LEVEL_CATEGORIES,
    LEVEL_SUBCATEGORIES
)
from app.db.models import Category, Subcategory
from app.db.requests.get_requests import (
    get_content_item_by_subcategory_id
)
from app.bot.filters.chat_types import ChatTypeFilter



user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))
user_private_router.callback_query.filter(ChatTypeFilter(["private"]))

user_menu_messages: Dict[int, Dict[str, Optional[int]]] = {}

async def delete_safe(bot, chat_id: int, message_id: Optional[int]):
    """Безопасное удаление сообщения."""
    if message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logging.info(f"Successfully deleted message {message_id} in chat {chat_id}")
            return True
        except Exception as e:
            logging.error(f"Failed to delete message {message_id} in chat {chat_id}: {e}")
    return False

@user_private_router.message(CommandStart())
async def start_command(msg: Message):
    """Обработчик команды /start. Показывает приветствие и кнопку Меню."""
    user_id = msg.from_user.id
    chat_id = msg.chat.id

    if user_id in user_menu_messages:
        logging.info(f"Cleaning up old menu messages for user {user_id}")
        await delete_safe(msg.bot, chat_id, user_menu_messages[user_id].get('content_msg_id'))
        await delete_safe(msg.bot, chat_id, user_menu_messages[user_id].get('submenu_msg_id'))
        await delete_safe(msg.bot, chat_id, user_menu_messages[user_id].get('main_menu_msg_id'))
        user_menu_messages[user_id] = {
            'main_menu_msg_id': None,
            'submenu_msg_id': None,
            'content_msg_id': None
        }

    text = """
👋 Здравствуйте! Вас приветствует бот сообщества BlockSide

🔥Мы команда единомышленников, объединенных идеей заработка криптовалюты. Данный бот поможет Вам начать ориентирроваться и сформировать инфополе, на правильных исходных принципах. Основная задача выстроить СИСТЕМНУЮ работы, используя инструменты масштабирующие Ваш результат.

Если кратко.....🚀 это  👥⌛️🎓💽💶👉🔧📈🎯


❗️ Что от Вас ожидается?

▪️Задавать больше уточняющих вопросов
▪️Задавать больше уточняющих вопросов
▪️Задавать больше уточняющих вопросов
▪️Исповедовать принцип "Узнал - попробовал"
▪️Увидел активность - сделал сразу.      
▪️Отмечать свое продвижение маленькими шажочками
▪️Свои результаты сравниваем с собственными некоторое время назад.


Добро пожаловать в Кузницу START🏁
"""
    start_menu_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Меню", callback_data="start_action")]
        ]
    )
    await msg.answer(text, reply_markup=start_menu_button)


@user_private_router.callback_query(F.data == 'start_action')
async def handle_start_action(callback: types.CallbackQuery, db_session: AsyncSession):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    if user_id in user_menu_messages:
        await delete_safe(callback.bot, chat_id, user_menu_messages[user_id].get('content_msg_id'))
        await delete_safe(callback.bot, chat_id, user_menu_messages[user_id].get('submenu_msg_id'))
        await delete_safe(callback.bot, chat_id, user_menu_messages[user_id].get('main_menu_msg_id'))

    keyboard = await build_main_menu_keyboard(db_session)
    if not keyboard or not keyboard.inline_keyboard:
        await callback.answer("Извините, меню пока не настроено.", show_alert=True)
        return

    main_menu_msg = await callback.message.answer("Добро пожаловать! Выберите раздел:", reply_markup=keyboard)

    user_menu_messages[user_id] = {
        'main_menu_msg_id': main_menu_msg.message_id,
        'submenu_msg_id': None,
        'content_msg_id': None
    }
    await callback.answer()


@user_private_router.message(Command("menu"))
async def show_main_menu(message: types.Message, db_session: AsyncSession):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id in user_menu_messages:
        await delete_safe(message.bot, chat_id, user_menu_messages[user_id].get('content_msg_id'))
        await delete_safe(message.bot, chat_id, user_menu_messages[user_id].get('submenu_msg_id'))
        await delete_safe(message.bot, chat_id, user_menu_messages[user_id].get('main_menu_msg_id'))

    keyboard = await build_main_menu_keyboard(db_session)
    if not keyboard or not keyboard.inline_keyboard:
        await message.answer("Извините, меню пока не настроено.")
        return
    
    main_menu_msg = await message.answer("Добро пожаловать! Выберите раздел:", reply_markup=keyboard)

    user_menu_messages[user_id] = {
        'main_menu_msg_id': main_menu_msg.message_id,
        'submenu_msg_id': None,
        'content_msg_id': None
    }


@user_private_router.callback_query(UserMenuCallbackData.filter(F.level == LEVEL_CATEGORIES))
async def navigate_to_submenu(callback: types.CallbackQuery, callback_data: UserMenuCallbackData, db_session: AsyncSession):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    category_id = callback_data.category_id

    user_msgs = user_menu_messages.setdefault(user_id, {})

    await delete_safe(callback.bot, chat_id, user_msgs.get('content_msg_id'))
    await delete_safe(callback.bot, chat_id, user_msgs.get('submenu_msg_id'))

    keyboard = await build_submenu_keyboard(category_id, db_session)
    category = await db_session.get(Category, category_id)
    category_name = category.name if category else "Раздел"

    if not keyboard or not keyboard.inline_keyboard:
        submenu_msg = await callback.message.answer(f"{category_name}: \n\nВ этом разделе пока ничего нет.")
        user_msgs['submenu_msg_id'] = submenu_msg.message_id
        user_msgs['content_msg_id'] = None
    else:
        submenu_msg = await callback.message.answer(
            f"Вы выбрали: {category_name}\n\nТеперь выберите подраздел:",
            reply_markup=keyboard
        )
        user_msgs['submenu_msg_id'] = submenu_msg.message_id
        user_msgs['content_msg_id'] = None

    await callback.answer()


@user_private_router.callback_query(UserMenuCallbackData.filter(F.level == LEVEL_SUBCATEGORIES))
async def show_content(callback: types.CallbackQuery, callback_data: UserMenuCallbackData, db_session: AsyncSession):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    subcategory_id = callback_data.subcategory_id

    user_msgs = user_menu_messages.setdefault(user_id, {})

    await delete_safe(callback.bot, chat_id, user_msgs.get('content_msg_id'))

    content_item = await get_content_item_by_subcategory_id(
        session=db_session,
        subcategory_id=subcategory_id
    )

    if content_item:
        content_msg = await callback.message.answer(
            text=content_item.text_content,
            reply_markup=None
        )
        user_msgs['content_msg_id'] = content_msg.message_id
    else:
        subcategory = await db_session.get(Subcategory, subcategory_id)
        subcategory_name = subcategory.name if subcategory else "Подраздел"
        content_msg = await callback.message.answer(
            f"Извините, для подраздела '{subcategory_name}' контент еще не добавлен.",
            reply_markup=None
        )
        user_msgs['content_msg_id'] = content_msg.message_id

    await callback.answer()