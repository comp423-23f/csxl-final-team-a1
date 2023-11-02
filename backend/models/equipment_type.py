from pydantic import BaseModel


class EquipmentType(BaseModel):
    """
    Pydantic model to represent how `EquipmentType`s are identified in the system.

    This model is based on

    """

    id: int | None = None
    title: str = ""
    description: str = ""
    max_reservation_time: int = 3
