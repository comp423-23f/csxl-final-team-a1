from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from ...models.equipment.equipment_item import EquipmentItem
from ...models.equipment.item_details import ItemDetails

class EquipmentItemEntity(EntityBase):
    """Serves as the database component for individual items"""

    # Name of the table
    __tablename__ = "equipment-items"

    # Unique ID for the item
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Stores if the item is to be displayed on the webpage
    # NOTE: This may be able to be auto calculated in the future via checkin/out table
    display_status: Mapped[bool] = mapped_column(Boolean, nullable= False)

    # Type of this item
    type_id: Mapped[int] = mapped_column(ForeignKey("equipment-type.id"))
    eq_type: Mapped["EquipmentTypeEntity"] = relationship(back_populates="items")

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
            type_id=model.type_id
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
            type_id=self.type_id
        )
    
    def to_details_model(self) -> ItemDetails:
        """
        Converts an EquipmentItemEntity into a ItemDetails model

        Returns:
            ItemDetails: Details model of entity
        """
        return ItemDetails(
            id=self.id,
            display_status=self.display_status,
            type_id=self.type_id,
            equipment_type=self.eq_type.to_model()
        )