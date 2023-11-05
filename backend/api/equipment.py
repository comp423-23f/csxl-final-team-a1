from fastapi import APIRouter, Depends
from .authentication import authenticated_pid
from ..services.equipment import EquipmentService, EquipmentType, EquipmentItem
from ..services import UserService
from ..models import UserDetails, User

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Equipment Reservation System",
    "description": "Reservation system that allow students to reserve lab-owned equipments for multiple days.",
}

# NOTE: Make sure to add tags to all subsequent api calls for them to show in /docs


@api.get("/list-all-equipments", tags=["Equipment Reservation System"])
def list_all_equipments(
    equipment_service: EquipmentService = Depends(),
) -> list[EquipmentType]:
    """
    Gets all Types and their associated availability

    Returns:
        dict[EquipmentType: int] - Type Model maps to the amount of items available
    """
    return equipment_service.get_all_types()

@api.put("/update-user-agreement-status", tags=["Equipment Reservation System"])
def update_user_agreement_status(
    pid_onyen: tuple[int, str] = Depends(authenticated_pid),
    user_svc: UserService = Depends()):
    """
    Updates a User's agreement_status field to be true

    Returns:
        UserDetails - the updated UserDetails object
    """
    pid, _ = pid_onyen
    user = user_svc.get(pid)
    if user is None:
        raise Exception("User not found!")

    user.agreement_status = True
    user = user_svc.update(user, user)

    user_details = user_svc.get(user.pid)
    if user_details:
        return user_details
    else:
        raise Exception("Unexpected internal server error.")