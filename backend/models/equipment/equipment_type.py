from pydantic import BaseModel


class EquipmentType(BaseModel):
    """
    Pydantic model to represent how `EquipmentType`s are identified in the system.

    This model is based on the `EquipmentTypeEntity` model, which defines the shape
    of the `EquipmentType` database in the PostgreSQL database.

    """

    id: int | None = None
    title: str = ""
    img_url: str = ""
    num_available: int = 0
    description: str = ""
    max_reservation_time: int = 3

