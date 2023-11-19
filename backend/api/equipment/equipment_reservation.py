from fastapi import APIRouter, Depends, HTTPException
from ..authentication import authenticated_pid
from ...services.equipment import EquipmentService, EquipmentType, EquipmentItem
from ...services import UserService, ResourceNotFoundException
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
        list[EquipmentType]: List of EquipmentTypes, which includes the current availability computing at the model level
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
    type_id: int,
    equipment_service: EquipmentService = Depends()
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
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put("/update-user-agreement-status", tags=["Equipment Reservation System"])
def update_user_agreement_status(
    pid_onyen: tuple[int, str] = Depends(authenticated_pid),
    user_service: UserService = Depends()
) -> UserDetails:
    """
    Updates a User's agreement_status field to be true

    Returns:
        UserDetails - the updated UserDetails object
    """
    pid, _ = pid_onyen
    user = user_service.get(pid)
    if user is None:
        raise Exception("User not found!")

    user.agreement_status = True
    user = user_service.update(user, user)

    user_details = user_service.get(user.pid)
    if user_details:
        return user_details
    else:
        raise Exception("Unexpected internal server error.")

