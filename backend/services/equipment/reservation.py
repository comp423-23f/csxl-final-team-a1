"""
The Reservation Service allows the API to manipulate equipment reservation related data in the database
"""


from datetime import datetime, timedelta
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.entities.equipment.reservation_entity import EquipmentReservationEntity
from backend.models.equipment.equipment_reservation import (
    EquipmentReservation,
    ReservationDetails,
)
from backend.models.user import User
from backend.services.equipment.equipment import EquipmentService

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
        type_id: int,
    ) -> list[ReservationDetails]:
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
    ) -> list[ReservationDetails]:
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
        reservation: EquipmentReservation,
        subject: User,
    ) -> ReservationDetails:
        """
        Create a reservation and save it to the database.

        Parameters:
            reservation: some data in the form of EquipmentReservation.
        """
        # Check that correct user is authenticated
        if reservation.user_id != subject.id:
            raise Exception("Not authenticated as correct user")

        # Check that user has no active reservations
        query = (
            select(EquipmentReservationEntity)
            .where(EquipmentReservationEntity.user_id == subject.id)
            .where(EquipmentReservationEntity.actual_return_date == None)
        )
        user_reservations = self._session.scalars(query).all()
        if len(user_reservations) >= 1:
            raise Exception("User already has active reservation(s)")

        # Check that checkout date is not before current day
        if datetime.now().date() > reservation.check_out_date.date():
            raise Exception("Checkout date is in the past")
        
        # Check that checkout date is before or at the same time as expected return
        if reservation.check_out_date > reservation.expected_return_date:
            raise Exception("Checkout is after return")
        
        # Check that return date is not more than 7 days from current day
        if reservation.expected_return_date.date() > datetime.now().date() + timedelta(days=7):
            raise Exception("Return date is too far in the future")
        
        # Check if type_id has item and exists
        query = select(EquipmentTypeEntity).where(
            EquipmentTypeEntity.id == reservation.type_id
        )
        type_entity = self._session.scalars(query).first()
        if type_entity == None:
            raise KeyError("Type id does not exist.")
        if reservation.item_id not in [item.id for item in type_entity.items]:
            raise ValueError("Type does not have item.")

        # Check if max checkout time exceeded
        if reservation.expected_return_date.date() - reservation.check_out_date.date() > timedelta(days=type_entity.max_time):
            raise Exception("Checkout for too many days")
        
        # Check to make sure some variables are empty
        if reservation.actual_return_date != None or reservation.ambassador_check_out or reservation.return_description != "":
            raise Exception("Illegal values set")

        query = select(EquipmentItemEntity).where(
            EquipmentItemEntity.id == reservation.item_id
        )
        item = self._session.scalars(query).first()
        if not item.display_status:
            raise NameError("Item not available")

        reservation.item_id = self.find_available_item(reservation, reservation.item_id)
        if reservation.item_id == -1:
            raise NameError("Item not available")

        entity = EquipmentReservationEntity.from_model(reservation)
        self._session.add(entity)
        self._session.commit()

        return entity.to_details_model()

    def find_available_item(
        self,
        reservation: EquipmentReservation,
        item_id: int,
    ) -> int:
        check_out = int(reservation.check_out_date.strftime("%j"))
        expected_return = int(reservation.expected_return_date.strftime("%j"))

        available: bool
        active_reservations = (
            self._session.query(EquipmentReservationEntity)
            .where(EquipmentReservationEntity.item_id == item_id)
            .where(EquipmentReservationEntity.actual_return_date==None)
            .all()
        )
        available = True

        for res in active_reservations:
            res_check_out = int(res.check_out_date.strftime("%j"))
            res_expected_return = int(res.expected_return_date.strftime("%j"))
            if (
                (res_check_out <= check_out and check_out <= res_expected_return)
                or (
                    res_check_out <= expected_return
                    and expected_return <= res_expected_return
                )
                or (
                    res_check_out >= check_out
                    and res_expected_return <= expected_return
                )
            ):
                available = False

        if available:
            return item_id

        return -1

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
        subject: User,
    ) -> bool:
        """
        Cancel a reservation by providing its id.

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

        if entity.user_id != subject.id:
            raise Exception("Not authenticated as correct user")

        if entity.actual_return_date == None and not entity.ambassador_check_out:
            self._session.delete(entity)
            self._session.commit()

            return True

        return False

    def check_in_equipment(
        self, id: int, return_date: datetime, description: str, subject: User
    ) -> ReservationDetails:
        """
        Update a reservation deactivate ambassador_check_out, add actual_return_date, and add a return_description.

        Parameters:
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
    ) -> list[ReservationDetails]:
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
    ) -> ReservationDetails:
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

    def ambassador_cancel_reservation(self, subject: User, id: int) -> bool:
        """
        Cancel a reservation by providing its id.

        Parameters:
            subject: user that will be checked for permission
            id: id number of reservation

        Returns:
            bool: depending on the success of cancellation
        """
        self._permission_svc.enforce(subject, "equipment.reservation", "equipment")

        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.id == id
        )

        entity = self._session.scalars(query).first()
        self._session.delete(entity)
        self._session.commit()

        return True
