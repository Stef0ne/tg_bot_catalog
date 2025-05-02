from aiogram.filters.callback_data import CallbackData


class SectionMenuCallbackData(CallbackData, prefix="section_menu"):
    level: int
    category_id: int | None = None
    subcategory_id: int | None = None 

class UserMenuCallbackData(SectionMenuCallbackData, prefix="user_menu"):
    pass
    
    
class AdminUserCallbackData(CallbackData, prefix="admin_user"):
    action: str 
    

class AdminSectionCallbackData(CallbackData, prefix="admin_section"):
    action: str
    category_id: int | None = None
    subcategory_id: int | None = None
    
    
class AdminMenuCallbackData(SectionMenuCallbackData, prefix="admin_menu"):
    pass