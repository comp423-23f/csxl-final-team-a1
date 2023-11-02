from pydantic import BaseModel
from .equipment_type import EquipmentType


class EquipmentItem(BaseModel):
    """

    Pydantic model to represent how `EquipmentItem`s are identified in the system.

    This model is based on the `EquipmentItemEntity` model, which defines the shape
    of the `EquipmentItem` database in the PostgreSQL database.

    """

    id: int | None = None
    equipment_type: EquipmentType
    display_status: bool = True
