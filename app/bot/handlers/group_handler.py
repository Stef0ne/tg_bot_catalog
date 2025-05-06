from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.keyboard_admin import (
    LEVEL_CATEGORIES,
    LEVEL_SUBCATEGORIES,
    get_main_manage_keyboard, 
    get_user_management_keyboard,
    get_section_management_keyboard,
    get_cancel_button_fsm,
    get_subcategory_management_keyboard,
    get_content_management_keyboard,
    get_add_section_confirmation_keyboard,
    get_edit_section_confirmation_keyboard,
    get_delete_section_confirmation_keyboard,
    get_add_subsection_confirmation_keyboard,
    get_edit_subsection_confirmation_keyboard,
    get_delete_subsection_confirmation_keyboard,
    get_add_content_item_confirmation_keyboard,
    get_edit_content_item_confirmation_keyboard,
    get_cancel_button_for_users
)
from app.bot.callbacks.menu_callback import AdminUserCallbackData, AdminSectionCallbackData, AdminMenuCallbackData
from app.db.requests.get_requests import (
    get_content_item_by_subcategory_id,
    get_category_by_id,
    get_subcategory_by_id,
    get_all_users,
    get_user_by_telegram_id
)
from app.db.requests.create_requests import (
    create_category, 
    create_subcategory,
    create_content_item,
    create_user
)
from app.db.requests.update_requests import (
    update_category_name,
    update_subcategory_name,
    update_content_item_text
)
from app.db.requests.delete_requests import (
    delete_category,
    delete_subcategory,
    delete_user
)
from app.bot.states.states import (
    AdminAddSectionState,
    AdminEditSectionState,
    AdminDeleteSectionState,
    AdminAddSubsectionState,
    AdminEditSubsectionState,
    AdminDeleteSubsectionState,
    AdminAddContentItemState,
    AdminEditContentItemState,
    AdminAddUserState,
    AdminDeleteUserState
)



#GROUP_ID=-4776121612
GROUP_ID = -4679067194

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
async def show_user_management_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Управление пользователями:", reply_markup=get_user_management_keyboard())
    await callback.answer()

@group_router.callback_query(AdminUserCallbackData.filter(F.action == "list"))
async def handle_users_list(callback: types.CallbackQuery, db_session: AsyncSession):
    users = await get_all_users(session=db_session)
    users_text = "\n".join([f"{user.username} - {user.telegram_id}" for user in users])
    await callback.message.edit_text(users_text, reply_markup=get_user_management_keyboard()) 
    await callback.answer()

@group_router.callback_query(AdminUserCallbackData.filter(F.action == "add_user"))
async def handle_users_add_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Напишите ID.", 
        reply_markup=get_cancel_button_for_users()
    )
    await state.set_state(AdminAddUserState.waiting_for_id)
    await callback.answer()
    
@group_router.message(AdminAddUserState.waiting_for_id)
async def handle_user_id_input_add(message: types.Message, state: FSMContext, db_session: AsyncSession):
    user_id_str = message.text.strip()
    if not user_id_str.isdigit():
        await message.answer("Пожалуйста, введите корректный ID.")
        return
    user_id = int(user_id_str)
    new_user = await create_user(session=db_session, telegram_id=user_id)
    await state.clear()
    if new_user:
        await message.answer(
            f"Пользователь с ID `{user_id}` успешно добавлен!",
            reply_markup=get_user_management_keyboard()
        )
    else:
        existing_user = await get_user_by_telegram_id(session=db_session, telegram_id=user_id)
        if existing_user:
             await message.answer(
                f"Пользователь с ID `{user_id}` уже существует в базе.",
                reply_markup=get_user_management_keyboard()
            )
        else:
            await message.answer(
                f"Произошла ошибка при добавлении пользователя с ID `{user_id}`.",
                reply_markup=get_user_management_keyboard()
            )

@group_router.callback_query(AdminUserCallbackData.filter(F.action == "delete_user"))
async def handle_users_delete_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Напишите id пользователя для удаления", 
        reply_markup=get_cancel_button_for_users()
    )
    await state.set_state(AdminDeleteUserState.waiting_for_id)
    await callback.answer()
    
@group_router.message(AdminDeleteUserState.waiting_for_id)
async def handle_user_id_input_delete(message: types.Message, state: FSMContext, db_session: AsyncSession):
    user_id_str = message.text.strip()
    if not user_id_str.isdigit():
        await message.answer("Пожалуйста, введите корректный ID.")
        return
    user_id = int(user_id_str)
    user = await get_user_by_telegram_id(session=db_session, telegram_id=user_id)
    if user:
        await delete_user(session=db_session, telegram_id=user_id)
        await message.answer(
            f"Пользователь с id: {user_id} удален.",
            reply_markup=get_user_management_keyboard()
        )
    else:
        await message.answer(
            f"Пользователь с id: {user_id} не найден.",
            reply_markup=get_user_management_keyboard()
        )
    
@group_router.callback_query(AdminUserCallbackData.filter(F.action == "back"))
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "back"))
async def handle_back_to_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=get_main_manage_keyboard()
    )
    await callback.answer()
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "manage"))
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "back_subcategory"))
async def show_category_management_menu(callback: types.CallbackQuery, db_session: AsyncSession, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Выберите раздел или добавьте новый:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await callback.answer()
    
@group_router.callback_query(AdminMenuCallbackData.filter(F.level == LEVEL_CATEGORIES))
async def show_subcategory_management_menu(callback: types.CallbackQuery, callback_data: AdminMenuCallbackData, db_session: AsyncSession):
    category_id = callback_data.category_id
    await callback.message.edit_text(
        "Выберите раздел для редактирования или добавьте новый подраздел:",
        reply_markup=await get_subcategory_management_keyboard(category_id=category_id, session=db_session)
    )
    await callback.answer()
    
@group_router.callback_query(AdminMenuCallbackData.filter(F.level == LEVEL_SUBCATEGORIES))
async def show_content_management_menu(callback: types.CallbackQuery, callback_data: AdminMenuCallbackData, db_session: AsyncSession):
    subcategory_id = callback_data.subcategory_id
    content_item = await get_content_item_by_subcategory_id(
        session=db_session,
        subcategory_id=subcategory_id
    )
    if content_item:
        await callback.message.edit_text(
            text=f"Выберите действие с контентом:\n\n{content_item.text_content}",
            reply_markup=await get_content_management_keyboard(subcategory_id=subcategory_id, session=db_session)
        )
    else:
        await callback.message.edit_text(
            "В этом подразделе нет контента. Выберите действие:",
            reply_markup=await get_content_management_keyboard(subcategory_id=subcategory_id, session=db_session)
        )
    await callback.answer()
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "add_category"))
async def handle_add_section(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Введите название нового раздела:",
        reply_markup=get_cancel_button_fsm()
    )
    await state.set_state(AdminAddSectionState.waiting_for_name)
    await callback.answer()
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "cancel_fsm"))
async def handle_cancel_add_section(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    await state.clear()
    await callback.message.edit_text(
        "Действие отменено. Выберите раздел для редактирования или добавьте новый:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await callback.answer("Отменено")
    
@group_router.message(AdminAddSectionState.waiting_for_name)
async def handle_section_name_input(message: types.Message, state: FSMContext):
    section_name = message.text.strip()
    if not section_name:
        await message.answer("Название раздела не может быть пустым. Попробуйте еще раз или нажмите 'Отмена'.")
        return
    await state.update_data(section_name=section_name)
    await message.answer(
        f"Вы хотите создать раздел с названием: '{section_name}'?",
        reply_markup=get_add_section_confirmation_keyboard()
    )
    await state.set_state(AdminAddSectionState.waiting_for_confirmation)
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_add_category"), AdminAddSectionState.waiting_for_confirmation)
async def handle_confirm_add_section(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    section_name = user_data.get('section_name')
    if not section_name:
        await callback.answer("Ошибка: Не удалось получить название раздела.", show_alert=True)
        await state.clear()
        await callback.message.edit_text(
             "Произошла ошибка. Выберите раздел для редактирования или добавьте новый:",
             reply_markup=await get_section_management_keyboard(session=db_session)
        )
        return
    await create_category(session=db_session, name=section_name)
    await callback.message.edit_text(
        f"Раздел '{section_name}' успешно создан!\n\nУправление разделами:", 
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await state.clear()
    # await callback.message.answer(
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )
    await callback.answer("Раздел создан")
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "edit_category"))
async def handle_edit_category_start(callback: types.CallbackQuery, callback_data: AdminSectionCallbackData, state: FSMContext, db_session: AsyncSession):
    category_id = callback_data.category_id
    category = await get_category_by_id(session=db_session, category_id=category_id)
    current_name = category.name
    await state.update_data(category_id=category_id, current_name=current_name)
    await callback.message.edit_text(
        f"Редактирование раздела: '{current_name}'.\n\nВведите новое название:",
        reply_markup=get_cancel_button_fsm()
    )
    await state.set_state(AdminEditSectionState.waiting_for_new_name)
    await callback.answer()   

@group_router.message(AdminEditSectionState.waiting_for_new_name)
async def handle_edit_category_name_input(message: types.Message, state: FSMContext):
    new_name = message.text.strip()
    if not new_name:
        await message.answer(
            "Название категории не может быть пустым. Попробуйте еще раз или нажмите 'Отмена'."
            )
        return 
    user_data = await state.get_data()
    current_name = user_data.get('current_name')
    await state.update_data(new_section_name=new_name)
    await message.answer(
        f"Вы уверены, что хотите переименовать категорию:\n"
        f"'{current_name}' -> '{new_name}'?",
        reply_markup=get_edit_section_confirmation_keyboard()
    )
    await state.set_state(AdminEditSectionState.waiting_for_confirmation)

@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_edit_category"), AdminEditSectionState.waiting_for_confirmation)
async def handle_confirm_edit_category(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    category_id = user_data.get('category_id')
    new_name = user_data.get('new_section_name')
    await update_category_name(session=db_session, category_id=category_id, new_name=new_name)
    await state.clear()
    await callback.message.edit_text(
        f"Название категории успешно изменено на '{new_name}'.\n\nУправление разделами:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await callback.answer("Подтверждено")
    # await callback.message.answer( 
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "delete_category"))
async def handle_delete_category_start(callback: types.CallbackQuery, callback_data: AdminSectionCallbackData, state: FSMContext, db_session: AsyncSession):
    category_id = callback_data.category_id
    category = await get_category_by_id(session=db_session, category_id=category_id)
    current_name = category.name
    await state.update_data(category_id=category_id, current_name=current_name)
    await callback.message.edit_text(
        f"Уверены, что хотите удалить раздел: '{current_name}'?",
        reply_markup=get_delete_section_confirmation_keyboard()
    )
    await state.set_state(AdminDeleteSectionState.waiting_for_confirmation)
    await callback.answer()   

@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_delete_category"), AdminDeleteSectionState.waiting_for_confirmation)
async def handle_confirm_delete_category(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    category_id = user_data.get('category_id')
    current_name = user_data.get('current_name')
    await delete_category(session=db_session, category_id=category_id)
    await state.clear()
    await callback.message.edit_text(
        f"Раздел '{current_name}' успешно удален.\n\nУправление разделами:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await callback.answer("Удалено")
    # await callback.message.answer( 
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )

@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "add_subcategory"))
async def handle_add_subcategory(callback: types.CallbackQuery, callback_data: AdminSectionCallbackData, state: FSMContext, db_session: AsyncSession):
    category_id = callback_data.category_id
    category = await get_category_by_id(session=db_session, category_id=category_id)
    await callback.message.edit_text(
        f"Введите название нового подраздела для раздела: '{category.name}':",
        reply_markup=get_cancel_button_fsm()
    )
    await state.update_data(category_id=category_id)
    await state.set_state(AdminAddSubsectionState.waiting_for_name)
    await callback.answer()
    
@group_router.message(AdminAddSubsectionState.waiting_for_name)
async def handle_subcategory_name_input(message: types.Message, state: FSMContext):
    subsection_name = message.text.strip()
    if not subsection_name:
        await message.answer("Название подраздела не может быть пустым. Попробуйте еще раз или нажмите 'Отмена'.")
        return
    await state.update_data(subsection_name=subsection_name)
    await message.answer(
        f"Вы хотите создать подраздел с названием: '{subsection_name}'?",
        reply_markup=get_add_subsection_confirmation_keyboard()
    )
    await state.set_state(AdminAddSubsectionState.waiting_for_confirmation)
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_add_subcategory"), AdminAddSubsectionState.waiting_for_confirmation)
async def handle_confirm_add_subsection(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    subsection_name = user_data.get('subsection_name')
    category_id = user_data.get('category_id')
    if not subsection_name:
        await callback.answer("Ошибка: Не удалось получить название подраздела.", show_alert=True)
        await state.clear()
        await callback.message.edit_text(
             "Произошла ошибка. Выберите раздел для редактирования или добавьте новый:",
             reply_markup=await get_section_management_keyboard(session=db_session)
        )
        return
    await create_subcategory(session=db_session, name=subsection_name, category_id=category_id)
    await callback.message.edit_text(
        f"Подраздел '{subsection_name}' успешно создан!\n\nУправление разделами:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await state.clear()
    # await callback.message.answer(
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )
    await callback.answer("Подраздел создан")

@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "edit_subcategory"))
async def handle_edit_subcategory_start(callback: types.CallbackQuery, callback_data: AdminSectionCallbackData, state: FSMContext, db_session: AsyncSession):
    subcategory_id = callback_data.subcategory_id
    subcategory = await get_subcategory_by_id(session=db_session, subcategory_id=subcategory_id)

    current_name = subcategory.name
    await state.update_data(subcategory_id=subcategory_id, current_name=current_name)
    await callback.message.edit_text(
        f"Редактирование подраздела: '{current_name}'.\n\nВведите новое название:",
        reply_markup=get_cancel_button_fsm()
    )
    await state.set_state(AdminEditSubsectionState.waiting_for_new_name)
    await callback.answer()   

@group_router.message(AdminEditSubsectionState.waiting_for_new_name)
async def handle_edit_subcategory_name_input(message: types.Message, state: FSMContext):
    new_name = message.text.strip()
    if not new_name:
        await message.answer(
            "Название подраздела не может быть пустым. Попробуйте еще раз или нажмите 'Отмена'."
            )
        return 
    user_data = await state.get_data()
    current_name = user_data.get('current_name')
    await state.update_data(new_subsection_name=new_name)
    await message.answer(
        f"Вы уверены, что хотите переименовать подрааздел:\n"
        f"'{current_name}' -> '{new_name}'?",
        reply_markup=get_edit_subsection_confirmation_keyboard()
    )
    await state.set_state(AdminEditSubsectionState.waiting_for_confirmation)

@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_edit_subcategory"), AdminEditSubsectionState.waiting_for_confirmation)
async def handle_confirm_edit_subcategory(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    subcategory_id = user_data.get('subcategory_id')
    new_name = user_data.get('new_subsection_name')
    await update_subcategory_name(session=db_session, subcategory_id=subcategory_id, new_name=new_name)
    await state.clear()
    await callback.message.edit_text(
        f"Название подкатегории успешно изменено на '{new_name}'.\n\nУправление разделами:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await callback.answer("Подтверждено")
    # await callback.message.answer( 
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "delete_subcategory"))
async def handle_delete_subcategory_start(callback: types.CallbackQuery, callback_data: AdminSectionCallbackData, state: FSMContext, db_session: AsyncSession):
    subcategory_id = callback_data.subcategory_id
    subcategory = await get_subcategory_by_id(session=db_session, subcategory_id=subcategory_id)
    current_name = subcategory.name
    await state.update_data(subcategory_id=subcategory_id, current_name=current_name)
    await callback.message.edit_text(
        f"Уверены, что хотите удалить подраздел: '{current_name}'?",
        reply_markup=get_delete_subsection_confirmation_keyboard()
    )
    await state.set_state(AdminDeleteSubsectionState.waiting_for_confirmation)
    await callback.answer()   

@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_delete_subcategory"), AdminDeleteSubsectionState.waiting_for_confirmation)
async def handle_confirm_delete_subcategory(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    subcategory_id = user_data.get('subcategory_id')
    current_name = user_data.get('current_name')
    await delete_subcategory(session=db_session, subcategory_id=subcategory_id)
    await state.clear()
    await callback.message.edit_text(
        f"Подраздел '{current_name}' успешно удален.\n\nУправление разделами:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await callback.answer("Удалено")
    # await callback.message.answer( 
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "add_content_item"))
async def handle_add_content_item(callback: types.CallbackQuery, callback_data: AdminSectionCallbackData, state: FSMContext, db_session: AsyncSession):
    subcategory_id = callback_data.subcategory_id
    subcategory = await get_subcategory_by_id(session=db_session, subcategory_id=subcategory_id)
    await callback.message.edit_text(
        f"Введите новый контент для подраздела: '{subcategory.name}':",
        reply_markup=get_cancel_button_fsm()
    )
    await state.update_data(subcategory_id=subcategory_id)
    await state.set_state(AdminAddContentItemState.waiting_for_content)
    await callback.answer()

@group_router.message(AdminAddContentItemState.waiting_for_content)
async def handle_content_item_name_input(message: types.Message, state: FSMContext):
    content_item_text = message.text.strip()
    if not content_item_text:
        await message.answer("Контент не может быть пустым. Попробуйте еще раз или нажмите 'Отмена'.")
        return
    await state.update_data(content_item_text=content_item_text)
    await message.answer(
        f"Новый контент будет такой:\n\n{content_item_text}",
        reply_markup=get_add_content_item_confirmation_keyboard()
    )
    await state.set_state(AdminAddContentItemState.waiting_for_confirmation)
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_add_content_item"), AdminAddContentItemState.waiting_for_confirmation)
async def handle_confirm_add_content_item(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    content_item_text = user_data.get('content_item_text')
    subcategory_id = user_data.get('subcategory_id')
    if not content_item_text:
        await callback.answer("Ошибка: Не удалось получить контент.", show_alert=True)
        await state.clear()
        await callback.message.edit_text(
             "Произошла ошибка. Выберите раздел для редактирования или добавьте новый:",
             reply_markup=await get_section_management_keyboard(session=db_session)
        )
        return
    await create_content_item(session=db_session, text_content=content_item_text, subcategory_id=subcategory_id)
    await callback.message.edit_text(
        f"Контент успешно создан!\n\nУправление разделами:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await state.clear()
    # await callback.message.answer(
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )
    await callback.answer("Контент создан")
    
@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "edit_content_item"))
async def handle_edit_content_item_start(callback: types.CallbackQuery, callback_data: AdminSectionCallbackData, state: FSMContext, db_session: AsyncSession):
    subcategory_id = callback_data.subcategory_id

    await state.update_data(subcategory_id=subcategory_id)
    await callback.message.edit_text(
        f"Введите новый контент:",
        reply_markup=get_cancel_button_fsm()
    )
    await state.set_state(AdminEditContentItemState.waiting_for_new_content)
    await callback.answer()   

@group_router.message(AdminEditContentItemState.waiting_for_new_content)
async def handle_edit_content_item_content_input(message: types.Message, state: FSMContext):
    new_content = message.text.strip()
    if not new_content:
        await message.answer(
            "Контент не может быть пустым. Попробуйте еще раз или нажмите 'Отмена'."
            )
        return 
    await state.update_data(new_content=new_content)
    await message.answer(
        "Вы уверены, что хотите изменить контент на введенный вами текст?",
        reply_markup=get_edit_content_item_confirmation_keyboard()
    )
    await state.set_state(AdminEditContentItemState.waiting_for_confirmation)

@group_router.callback_query(AdminSectionCallbackData.filter(F.action == "confirm_edit_content_item"), AdminEditContentItemState.waiting_for_confirmation)
async def handle_confirm_edit_subcategory(callback: types.CallbackQuery, state: FSMContext, db_session: AsyncSession):
    user_data = await state.get_data()
    subcategory_id = user_data.get('subcategory_id')
    new_content = user_data.get('new_content')
    await update_content_item_text(session=db_session, subcategory_id=subcategory_id, text_content=new_content)
    await state.clear()
    await callback.message.edit_text(
        f"Контент успешно изменен.\n\nУправление разделами:",
        reply_markup=await get_section_management_keyboard(session=db_session)
    )
    await callback.answer("Подтверждено")
    # await callback.message.answer( 
    #     "Управление разделами:",
    #     reply_markup=await get_section_management_keyboard(session=db_session)
    # )