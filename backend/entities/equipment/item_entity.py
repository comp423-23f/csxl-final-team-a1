from fastapi import Depends
from sqlalchemy import Integer, Boolean, ForeignKey, select, String
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from ...models.equipment.equipment_item import EquipmentItem
from ...models.equipment.item_details import ItemDetails


class EquipmentItemEntity(EntityBase):
    """Serves as the database component for individual items"""

    # Name of the table
    __tablename__ = "equipment_items"

    # Unique ID for the item
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Stores if the item is to be displayed on the webpage
    # NOTE: This may be able to be auto calculated in the future via checkin/out table
    display_status: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Type of this item
    type_id: Mapped[int] = mapped_column(ForeignKey("equipment_type.id"))
    eq_type: Mapped["EquipmentTypeEntity"] = relationship(back_populates="items")
    return_description: Mapped[str] = mapped_column(String, nullable=False)

    # Stores reservations in a one-to-many relationship
    equipment_reservations: Mapped[list["EquipmentReservationEntity"]] = relationship(
        back_populates="item"
    )

    @classmethod
    def from_model(cls, model: EquipmentItem) -> Self:
        """
        Class method that converts an EquipmentItem model into it's EquipmentTypeEntity

        Parameters:
            - model (EquipmentItem): Model that will be converted
        Returns:
            EquipmentItemEntity: Entity that was created
        """
        return cls(
            id=model.id,
            display_status=model.display_status,
            type_id=model.type_id,
            return_description=model.return_description,
        )

    def to_model(self) -> EquipmentItem:
        """
        Converts an EqupimentItemEntity into an EquipmentItem Model

        Returns:
            EquipmentItem: Model object from entity
        """
        return EquipmentItem(
            id=self.id,
            display_status=self.display_status,
            type_id=self.type_id,
            return_description=self.return_description,
        )
