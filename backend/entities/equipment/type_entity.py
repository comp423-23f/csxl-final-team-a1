from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from ...models.equipment import EquipmentType, TypeDetails


class EquipmentTypeEntity(EntityBase):
    """Database model for EquipmentTypes used throughout the Equipment Features"""

    # Name for the EquipmentType table in the PostgresSQL databse
    __tablename__ = "equipment_type"

    # Equipment Type Properties

    # Unique ID for the type
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Title for the type
    title: Mapped[str] = mapped_column(String, nullable=False)
    # Image URL for the Equipment Types image
    img_url: Mapped[str] = mapped_column(String, nullable=True)
    # Description for the item's type
    desc: Mapped[str] = mapped_column(String, nullable=True, default="")
    # Max reservation time for the item
    max_time: Mapped[int] = mapped_column(Integer, nullable=False, default=3)

    # Stores items in a One-to-Many relationship
    items: Mapped[list["EquipmentItemEntity"]] = relationship(back_populates="eq_type")

    # Stores reservations in a one-to-many relationship
    equipment_reservations: Mapped[list["EquipmentReservationEntity"]] = relationship(
        back_populates="equipment_type"
    )

    @classmethod
    def from_model(cls, model: EquipmentType) -> Self:
        """
        Class method that converts an EquipmentType model into an EquipmentTypeEntity

        Parameters:
            - model (EquipmentType): Model to convert into an entity
        Returns:
            EquipmentTypeEntity: Entity created from the model
        """

        return cls(
            id=model.id,
            title=model.title,
            img_url=model.img_url,
            desc=model.description,
            max_time=model.max_reservation_time,
        )

    def to_model(self) -> EquipmentType:
        """
        Converts an EquipmentTypeEntity object into an EquipmentType model object.

        Returns:
            EquipmentType: Object created from entity
        """
        available_items = [
            item.to_model() for item in self.items if item.display_status
        ]
        return EquipmentType(
            id=self.id,
            title=self.title,
            img_url=self.img_url,
            num_available=len(available_items),
            description=self.desc,
            max_reservation_time=self.max_time,
        )

    def to_details_model(self) -> TypeDetails:
        """
        Converts EquipmentTypeEntity into a TypeDetails model

        Returns:
            TypeDetails: Model version of Entity
        """
        available_items = [item.to_model() for item in self.items]
        return TypeDetails(
            id=self.id,
            title=self.title,
            img_url=self.img_url,
            num_available=len([1 for item in available_items if item.display_status]),
            description=self.desc,
            max_reservation_time=self.max_time,
            items=available_items,
        )
