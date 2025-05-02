from aiogram.fsm.state import State, StatesGroup


class AdminAddSectionState(StatesGroup):
    waiting_for_name = State()
    waiting_for_confirmation = State()
    

class AdminEditSectionState(StatesGroup):
    waiting_for_new_name = State()       
    waiting_for_confirmation = State()
    
    
class AdminDeleteSectionState(StatesGroup):
    waiting_for_confirmation = State()


class AdminAddSubsectionState(StatesGroup):
    waiting_for_name = State()
    waiting_for_confirmation = State()
    
    
class AdminEditSubsectionState(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_confirmation = State()
    

class AdminDeleteSubsectionState(StatesGroup):
    waiting_for_confirmation = State()


class AdminAddContentItemState(StatesGroup):
    waiting_for_content = State()
    waiting_for_confirmation = State()


class AdminEditContentItemState(StatesGroup):
    waiting_for_new_content = State()
    waiting_for_confirmation = State()