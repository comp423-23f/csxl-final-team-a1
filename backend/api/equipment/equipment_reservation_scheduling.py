from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta

from backend.models.equipment.equipment_reservation import (
    EquipmentReservation,
    ReservationDetails,
)
from backend.services.equipment.reservation import ReservationService
from backend.services.exceptions import UserPermissionException
from ..authentication import authenticated_pid, registered_user
from ...services import UserService, ResourceNotFoundException
from ...models import User

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Reservation Scheduling System",
    "description": "Scheduling system that allows students to check out equipment while ambassadors keep track.",
}


@api.get("/get-reservations/{type_id}", tags=["Reservation Scheduling System"])
def get_reservations(
    type_id: int,
    subject: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
) -> list[ReservationDetails]:
    """
    Get all reservations for all items of a specific type.

    Parameters:
        type_id: id of the type to retrieve items of

    Returns:
        list[EquipmentReservation]: list of reservations of the supplied type

    Raises:
        HTTP Exception 404 if the type cannot be found
        HTTP Exception 403 if no permissions
    """
    try:
        return reservation_service.get_reservations_by_type(subject, type_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.post("/create-reservation", tags=["Reservation Scheduling System"])
def create_reservation(
    reservation: EquipmentReservation,
    subject: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
) -> ReservationDetails:
    """
    Create a reservation and save it to the database.

    Parameters:
        reservation: some data in the form of EquipmentReservation.

    Returns:
        ReservationDetails: created reservation

    Raises:
        HTTP Exception 422 with details for any processing errors
        HTTP Exception 403 if user mismatch
        HTTP Exception 404 if the type or item can't be found
    """
    try:
        return reservation_service.create_reservation(reservation, subject)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.get("/ambassador-get-all-reservations", tags=["Reservation Scheduling System"])
def ambassador_get_all_reservations(
    subject: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
) -> list[ReservationDetails]:
    """
    Get all reservations as an ambassador.

    Returns:
        list[EquipmentReservation]: list of reservations

    Raises:
        HTTP Exception 403 if no permissions
    """
    try:
        return reservation_service.get_all_reservations(subject)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.get("/ambassador-get-active-reservations", tags=["Reservation Scheduling System"])
def ambassador_get_active_reservations(
    subject: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
) -> list[ReservationDetails]:
    """
    Get all active reservations as an ambassador.

    Returns:
        list[EquipmentReservation]: list of reservations where ambassador_check_out is True and actual_return_date is None.

    Raises:
        UserPermissionException - if user does not have permission
    """
    try:
        return reservation_service.get_active_reservations(subject)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.delete(
    "/ambassador-cancel-reservation/{reservation_id}",
    tags=["Reservation Scheduling System"],
)
def ambassador_cancel_reservation(
    reservation_id: int,
    subject: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
) -> bool:
    """
    Cancel a reservation that is inactive - as a student.

    Parameters:
        reservation_id: the id number of the reservation to cancel

    Returns:
        bool: depending on the success of cancellation

    Raises:
        HTTP Exception 404 if the reservation cannot be found
    """

    try:
        return reservation_service.ambassador_cancel_reservation(
            subject, reservation_id
        )
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.delete(
    "/cancel-reservation/{reservation_id}", tags=["Reservation Scheduling System"]
)
def cancel_reservation(
    reservation_id: int,
    subject: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
) -> bool:
    """
    Cancel a reservation that is inactive - as a student.

    Parameters:
        reservation_id: the id number of the reservation to cancel

    Returns:
        bool: depending on the success of cancellation

    Raises:
        HTTP Exception 404 if the reservation cannot be found
        HTTP Exception 403 if user mismatch
    """

    try:
        return reservation_service.cancel_reservation(reservation_id, subject)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@api.put(
    "/check-in-equipment/{reservation_id}/{description}",
    tags=["Reservation Scheduling System"],
)
def check_in_equipment(
    reservation_id: int,
    description: str,
    subject: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
) -> ReservationDetails:
    """
    Update a reservation deactivate ambassador_check_out, add actual_return_date, and add a return_description.

    Parameters:
        reservation_id: id number of the reservation to modify
        return_date: DateTime format of the actual return date
        description: string containing all information about the returned item's state

    Returns:
        EquipmentReservation: the model of the modified entity object

    Raises:
        HTTP Exception 404 if the reservation cannot be found
        HTTP Exception 403 if user mismatch
        HTTP Exception 422 if unprocessable
    """
    try:
        return reservation_service.check_in_equipment(
            reservation_id, datetime.now(), description, subject
        )
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.get("/get-user-equipment-reservations", tags=["Reservation Scheduling System"])
def get_user_equipment_reservations(
    reservation_service: ReservationService = Depends(),
    subject: User = Depends(registered_user),
) -> list[ReservationDetails]:
    """
    Gets all reservation details for a user

    Parameters:
        None (User subject automatically sent)

    Returns:
        list[ReservationDetails]: a list of ReservationDetails for the subject (requesting user)
    """
    return reservation_service.get_user_equipment_reservations(subject)


@api.put(
    "/activate-reservation/{reservation_id}", tags=["Reservation Scheduling System"]
)
def activate_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(),
    subject: User = Depends(registered_user),
) -> ReservationDetails:
    """
    Activates drafted reservation

    Parameters:
        reservation_id: Integer id of the reservation

    Returns:
        ReservationDetails: object of activated reservation

    Raises:
        HTTP Exception 404 if the reservation cannot be found
        HTTP Exception 403 if user mismatch

    """
    try:
        return reservation_service.activate_reservation(subject, reservation_id)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=e)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)
