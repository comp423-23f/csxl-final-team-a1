from fastapi import APIRouter, Depends, HTTPException
from ..authentication import authenticated_pid
from ...services.equipment import EquipmentService, EquipmentType, EquipmentItem
from ...services import UserService
from ...models import UserDetails, User
from ...models.equipment import TypeDetails

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


@api.get("/get-all", tags=["Equipment Reservation System"])
def get_all(equipment_service: EquipmentService = Depends()) -> list[TypeDetails]:
    """
    Gets all types and their associated items

    Returns:
        list[TypeDetails]: List of TypeDetails, which includes an EquipmentType and a list of EquipmentItems of that type
    """
    return equipment_service.get_all()


@api.get("/get-items-from-type", tags=["Equipment Reservation System"])
def get_items_from_type(
    type_id: int, equipment_service: EquipmentService = Depends()
) -> list[EquipmentItem]:
    """
    Gets all items of a specific type

    Parameters:
        type_id: id of the type to retrieve items of

    Returns:
        list[EquipmentItem]: list of items of the type supplied

    Raises:
        404: Type not found
    """
    try:
        return equipment_service.get_items_from_type(type_id)
    except Exception:
        raise HTTPException(404, "Type not found!")


@api.put("/update-user-agreement-status", tags=["Equipment Reservation System"])
def update_user_agreement_status(
    pid_onyen: tuple[int, str] = Depends(authenticated_pid),
    user_service: UserService = Depends(),
) -> bool:
    """
    Updates a User's agreement_status field to be true

    Returns:
        Boolean: the agreement_status field of the user
    """
    pid, _ = pid_onyen
    user = user_service.get(pid)
    if user is None:
        return False

    user.agreement_status = True
    user = user_service.update(user, user)

    user_details = user_service.get(user.pid)
    if user_details:
        return user_details.agreement_status

    return False


@api.get("/get-user-agreement-status/{pid}", tags=["Equipment Reservation System"])
def get_user_agreement_status(pid: int, user_service: UserService = Depends()) -> bool:
    """
    Returns the boolean value on if the User signed in has signed the equipment agreement

    Returns:
        Boolean: the agreement status of the User
    """
    user = user_service.get(pid)
    if user is None:
        return False

    user_details = user_service.get(user.pid)
    if user_details:
        return user_details.agreement_status

    return False
