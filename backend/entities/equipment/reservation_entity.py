from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.entities.equipment.item_entity import EquipmentItemEntity
from backend.entities.user_entity import UserEntity

from backend.models.equipment.equipment_reservation import ReservationDetails
from ..entity_base import EntityBase
from typing import Self
from ...models.equipment.equipment_reservation import EquipmentReservation
from datetime import datetime


class EquipmentReservationEntity(EntityBase):
    """Database model for EquipmentReservations which will be used throughout the equipment features"""

    # Name for the EquipmentReservation tabe in the database
    __tablename__ = "equipment-reservation"

    # Reservation Properties
    # Unique ID of the reservation
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # ID of the item which will be checked out
    # NOTE: This field establishes a one-to-many relationship between the equipment-items and equipment-reservation tables
    item_id: Mapped[int] = mapped_column(ForeignKey("equipment-items.id"))
    item: Mapped["EquipmentItemEntity"] = relationship(
        back_populates="resevations-items"
    )
    # ID of the user which will be checking out the item
    # NOTE: This establishes a one-to-many relationship between the user table and the equipment-reservation table
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="user-reservations")
    # Date that the reservation will be checked out at
    check_out_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # Indicates if the ambassador has handed the student the tech and checked it out
    ambassador_check_out: Mapped[bool] = mapped_column(Boolean, default=False)
    # Indicates the selected return date the user selected on initial reservation
    expected_return_date: Mapped[datetime] = mapped_column(DateTime)
    # Indicates if the user returned the object, and when
    actual_return_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Contains text for descirption of the state of the returned item of this reservation.
    return_description: Mapped[str | None] = mapped_column(String, nullable=True)

    @classmethod
    def from_model(cls, model: EquipmentReservation) -> Self:
        """
        Class method that converts an EquipmentReservation model into it's EquipmentReservationEntity

        Parameters:
            - model (EquipmentReservation): Model that will be converted
        Returns:
            EquipmentReservationEntity: Entity that was created
        """
        return cls(
            id=model.id,
            item_id=model.item_id,
            user_id=model.user_id,
            check_out_date=model.check_out_date,
            ambassador_check_out=model.ambassador_check_out,
            expected_return_date=model.expected_return_date,
            actual_return_date=model.actual_return_date,
            return_description=model.return_description,
        )

    def to_model(self) -> EquipmentReservation:
        """
        Class method that converts an EquipmenReservationEntity into an EquipmentReservation model.

        Returns:
            EquipmentReservation: Model object from entity
        """
        return EquipmentReservation(
            id=self.id,
            item_id=self.item_id,
            user_id=self.user_id,
            check_out_date=self.check_out_date,
            ambassador_check_out=self.ambassador_check_out,
            expected_return_date=self.expected_return_date,
            actual_return_date=self.actual_return_date,
            return_description=self.return_description,
        )

    @classmethod
    def from_details_model(cls, model: ReservationDetails) -> Self:
        """
        Class method that converts an EquipmentReservation model into it's EquipmentReservationEntity

        Parameters:
            - model (EquipmentReservation): Model that will be converted
        Returns:
            EquipmentReservationEntity: Entity that was created
        """
        return cls(
            id=model.id,
            item_id=model.item_id,
            user_id=model.user_id,
            check_out_date=model.check_out_date,
            ambassador_check_out=model.ambassador_check_out,
            expected_return_date=model.expected_return_date,
            actual_return_date=model.actual_return_date,
            return_description=model.return_description,
            item=model.item.id,
            user=model.user.id,
        )

    def to_details_model(self) -> ReservationDetails:
        """
        Class method that converts an EquipmentReservation model into it's EquipmentReservationEntity

        Parameters:
            - model (EquipmentReservation): Model that will be converted
        Returns:
            EquipmentReservationEntity: Entity that was created
        """
        return ReservationDetails(
            id=self.id,
            item_id=self.item_id,
            user_id=self.user_id,
            check_out_date=self.check_out_date,
            ambassador_check_out=self.ambassador_check_out,
            expected_return_date=self.expected_return_date,
            actual_return_date=self.actual_return_date,
            return_description=self.return_description,
            item=self.item.to_model(),
            user=self.user.to_model(),
        )
