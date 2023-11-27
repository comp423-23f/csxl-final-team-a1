from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..entity_base import EntityBase
from typing import Self
from ...models.equipment import EquipmentReservation
from datetime import datetime

class EquipmentReservationEntity(EntityBase):
    """Database model for EquipmentReservations which will be used throughout the equipment features"""

    # Name for the EquipmentReservation tabe in the database
    __tablename__ = "equipment-reservation"

    # Reservation Properties
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Unique ID of the reservation
    item_id: Mapped[int] = mapped_column(ForeignKey("equipment-items.id"))
    # ID of the item which will be checked out
    # NOTE: This field establishes a one-to-many relationship between the equipment-items and equipment-reservation tables
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # ID of the user which will be checking out the item
    # NOTE: This establishes a one-to-many relationship between the user table and the equipment-reservation table
    check_out_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # Date that the reservation will be checked out at
    ambassador_check_out: Mapped[bool] = mapped_column(Boolean, default=False)
    # Indicates if the ambassador has handed the student the tech and checked it out
    expected_return_date: Mapped[datetime] = mapped_column(DateTime)
    # Indicates the selected return date the user selected on initial reservation
    actual_return_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Indicates if the user returned the object, and when
    return_description: Mapped[str | None] = mapped_column(String, nullable=True)

    