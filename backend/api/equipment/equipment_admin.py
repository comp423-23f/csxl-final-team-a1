from fastapi import APIRouter, Depends

from backend.models.user import User
from ..authentication import authenticated_pid, registered_user
from ...services.equipment import EquipmentService, EquipmentType, EquipmentItem
from ...models.equipment.equipment_type import EquipmentType
from ...models.equipment.equipment_item import EquipmentItem
from ...models.equipment.item_details import ItemDetails
from ...models.equipment.type_details import TypeDetails

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Admin Equipment Reservation System",
    "description": "Admin-only system for adding, modifying, and deleting equipment from the system.",
}

# NOTE: Make sure to add tags to all subsequent api calls for them to show in /docs


@api.post("/add-equipment-type", tags=["Admin Equipment Reservation System"])
def add_equipment_type(
    equipment_type: EquipmentType,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentType:
    """
    Adds a new EquipmentType to the system

    Parameters:
        equipment_type (EquipmentType): The new EquipmentType to add
        subject (User): The user attempting the action
        equipment_service (EquipmentService): The Equipment backend service layer
    Returns:
        EquipmentType: The Equipment Type that was just added
    """
    return equipment_service.add_equipment_type(subject, equipment_type)


@api.put("/modify-equipment-type", tags=["Admin Equipment Reservation System"])
def modify_equipment_type(
    equipment_type: EquipmentType,
    id: int,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentType:
    """
    Modifies an existing EquipmentType object

    Parameters:
        equipment_type (EquipmentType): The new EquipmentType that will replace the old one
        id (int): The id of the EquipmentType to modify
        subject (User): The user attempting the action
        equipment_service (EquipmentService): The Equipment backend service layer
    Returns:
        EquipmentType: The Equipment Type that was just added
    """
    return equipment_service.modify_equipment_type(subject, id, equipment_type)


@api.delete("/delete-equipment-type", tags=["Admin Equipment Reservation System"])
def delete_equipment_type(
    id: int,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentType:
    """
    Deletes an EquipmentType object from the system

    Parameters:
        id (int): The id of the EquipmentType to delete
        subject (User): The user attempting the action
        equipment_service (EquipmentService): The Equipment backend service layer
    Returns:
        EquipmentType: The Equipment Type that was deleted
    """
    return equipment_service.delete_equipment_type(subject, id)
