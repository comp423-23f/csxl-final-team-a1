"""
The Reservation Service allows the API to manipulate equipment reservation related data in the database
"""


from datetime import datetime
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.entities.equipment.reservation_entity import EquipmentReservationEntity
from backend.models.equipment.equipment_reservation import (
    EquipmentReservation,
    ReservationDetails,
)
from backend.models.user import User

from backend.services.permission import PermissionService
from ...database import db_session

from ...entities import EquipmentItemEntity, EquipmentTypeEntity
from ...models import User


class ReservationService:
    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initialize the Reservation Service."""
        self._session = session
        self._permission_svc = permission_svc

    def get_reservations_by_type(
        self,
        subject: User,
        type_id: int,
    ) -> list[EquipmentReservation]:
        """
        Retrieves all reservations of specified type.

        Parameters:
            type_id: id of the type to retrieve items of

        Returns:
            list[EquipmentReservation]: list of reservations of the supplied type
        """
        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.type_id == type_id
        )
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]

    def get_all_reservations(
        self,
        subject: User,
    ) -> list[EquipmentReservation]:
        """
        Get all reservations.

        Returns:
            list[EquipmentReservation]: list of reservations
        """
        self._permission_svc.enforce(subject, "equipment.reservation", "equipment")

        query = select(EquipmentReservationEntity)

        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]

    def create_reservation(
        self,
        subject: User,
        reservation: EquipmentReservation,
    ) -> EquipmentReservation:
        """
        Create a reservation and save it to the database.

        Parameters:
            reservation: some data in the form of EquipmentReservation.
        """

        # TODO: check for overlapping reservations

        query = select(EquipmentItemEntity).where(
            EquipmentItemEntity.id == reservation.item_id
        )
        print(self._session.scalars(query).all())
        if self._session.scalars(query).all() == []:
            raise KeyError("Item id does not exist.")

        query = select(EquipmentTypeEntity).where(
            EquipmentTypeEntity.id == reservation.type_id
        )
        if self._session.scalars(query).all() == []:
            raise KeyError("Type id does not exist.")

        entity = EquipmentReservationEntity.from_model(reservation)
        self._session.add(entity)
        self._session.commit()

        return entity.to_details_model()

    def get_active_reservations(self, subject: User):
        """
        Get all active reservations.

        Parameters:
            subject: user that will be checked for permission

        Returns:
            list[EquipmentReservation]: list of reservations where ambassador_check_out is True and actual_return_date is None
        """
        self._permission_svc.enforce(subject, "equipment.reservation", "equipment")
        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.ambassador_check_out == True
        )
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]

    def cancel_reservation(
        self,
        id: int,
    ) -> bool:
        """
        Cancel a reserrvation by providing its id.

        Parameters:
            subject: user that will be checked for permission
            id: id number of reservation

        Returns:
            bool: depending on the success of cancellation
        """
        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.id == id
        )

        entity = self._session.scalars(query).first()

        if entity.actual_return_date == None and not entity.ambassador_check_out:
            self._session.delete(entity)
            self._session.commit()

            return True

        return False

    def check_in_equipment(
        self, id: int, return_date: datetime, description: str, subject: User
    ) -> EquipmentReservation:
        """
        Update a reservation deactivate ambassador_check_out, add actual_return_date, and add a return_description.

        Paramaters:
            id: id number of the reservation to modify
            return_date: DateTime format of the actual return date
            description: string containing all information about the returned item's state

        Returns:
            EquipmentReservation: the model of the modified entity object
        """
        self._permission_svc.enforce(subject, "equipment.reservation", "equipment")

        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.id == id
        )
        entity = self._session.scalars(query).first()

        if entity.ambassador_check_out and entity.actual_return_date == None:
            entity.ambassador_check_out = False
            entity.actual_return_date = return_date
            entity.return_description = description

        self._session.commit()

        return entity.to_details_model()

    def get_user_equipment_reservations(
        self, subject: User
    ) -> list[EquipmentReservation]:
        """
        Returns all reservation details for a user

        Parameters:
            subject: User
        """
        # Query reservation entity based on user ID
        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.user_id == subject.id
        )
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]

    def activate_reservation(
        self, subject: User, reservation_id: int
    ) -> EquipmentReservation:
        """
        Activates drafted reservation

        Parameters:
            reservation_id: Integer id of the reservation
        """
        self._permission_svc.enforce(subject, "equipment.reservation", "equipment")

        # Query reservation entity
        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.id == reservation_id
        )
        entity = self._session.scalars(query).first()

        entity.ambassador_check_out = True

        self._session.commit()
        return entity.to_details_model()
