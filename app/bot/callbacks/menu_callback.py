from aiogram.filters.callback_data import CallbackData


class MenuCallbackData(CallbackData, prefix="menu"):
    """
    Фабрика CallbackData для навигации по иерархическому меню.

    Атрибуты:
        level (int): Уровень меню (0: категории, 1: подкатегории, 2: контент).
        category_id (int | None): ID выбранной категории.
        subcategory_id (int | None): ID выбранной подкатегории.
        # action (str | None): Дополнительное действие (например, 'back').
    """
    level: int
    category_id: int | None = None
    subcategory_id: int | None = None
    # action: str | None = None # Раскомментируй, если нужно поле действия 
    
    
class AdminUserCallbackData(CallbackData, prefix="admin_user"):
    """
    Фабрика CallbackData для навигации по иерархическому меню администратора.
    """
    action: str 
    

class AdminSectionCallbackData(CallbackData, prefix="admin_section"):
    """
    Фабрика CallbackData для навигации по иерархическому меню администратора.
    """
    action: str
    
