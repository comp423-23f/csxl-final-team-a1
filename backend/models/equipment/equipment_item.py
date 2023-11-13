from pydantic import BaseModel


class EquipmentItem(BaseModel):
    """

    Pydantic model to represent how `EquipmentItem`s are identified in the system.

    This model is based on the `EquipmentItemEntity` model, which defines the shape
    of the `EquipmentItem` database in the PostgreSQL database.

    display_status - turns false on any event that the item is not available (i.e. is checked out or damaged)
    """

    id: int | None = None
    display_status: bool = True
    type_id: int