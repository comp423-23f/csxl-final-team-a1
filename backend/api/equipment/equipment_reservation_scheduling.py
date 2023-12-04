from fastapi import APIRouter, Depends, HTTPException
import datetime as dt

from backend.models.equipment.equipment_reservation import EquipmentReservation
from backend.services.equipment.reservation import ReservationService
from ..authentication import authenticated_pid, registered_user
from ...services.equipment.equipment import (
    EquipmentService,
    EquipmentType,
    EquipmentItem
)
from ...services import UserService, ResourceNotFoundException
from ...models import UserDetails, User
from ...models.equipment import TypeDetails

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Reservation Scheduling System",
    "description": "Scheduling system that allows students to check out equipment while ambassadors keep track.",
}

@api.get("/get-reservations", tags=["Reservation Scheduling System"])
def get_reservations(
    type_id: int, reservation_service: ReservationService = Depends()
) -> list[EquipmentReservation]:
    """
    Get all reservations for all items of a specific type.

    Parameters:
        type_id: id of the type to retrieve items of

    Returns:
        list[EquipmentReservation]: list of reservations of the supplied type
    """
    try:
        return reservation_service.get_reservations(type_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post("/create-reservation", tags=["Reservation Scheduling System"])
def create_reservation(
    reservation: EquipmentReservation,
    pid_onyen: tuple[int, str] = Depends(authenticated_pid),
    reservation_service: ReservationService = Depends(),
):
    """
    Create a reservation and save it to the database.

    Parameters:
        reservation: some data in the form of EquipmentReservation.
    """

@api.put("/activate-reservation", tags=["Reservation Scheduling System"])
def activate_reservation(
    reservation_id: int,
    reservation_service: ReservationService = Depends(),
    subject: User = Depends(registered_user),
):
    """
    Activates drafted reservation

    Parameters:
        reservation_id: Integer id of the reservation
    """
    reservation_service.activate_reservation(subject, reservation_id)

@api.get("/get-user-equipment-reservations", tags=["Reservation Scheduling System"])
def get_user_equipment_reservations(
    reservation_service: ReservationService = Depends(),
    subject: User = Depends(registered_user),
):
    """
    Gets all reservation details for a user

    Parameters:
        None (User subject automatically sent)
    """
    reservation_service.get_user_equipment_reservations(subject)



