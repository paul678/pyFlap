from enum import Enum


class AutomatonAction(Enum):
    Add_State = 1
    Delete_State = 2
    Add_Transition = 3
    Set_Initial = 4
    Set_Final = 5
    No_Action = -1
