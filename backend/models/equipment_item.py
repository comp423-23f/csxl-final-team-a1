from pydantic import BaseModel
from equipment_type import EquipmentType


class EquipmentItem(BaseModel):
    id: int | None = None
    equipment_type: EquipmentType
    display_status: bool = True
