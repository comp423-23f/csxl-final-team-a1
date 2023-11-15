from fastapi import APIRouter, Depends

from backend.models.user import User
from ..authentication import authenticated_pid, registered_user
from ...services.equipment import EquipmentService, EquipmentType, EquipmentItem
from ...models.equipment.equipment_type import EquipmentType
from ...models.equipment.equipment_item import EquipmentItem
from ...models.equipment.item_details import ItemDetails
from ...models.equipment.type_details import TypeDetails

api = APIRouter(prefix="/api/equipment/admin")
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

    Returns:
        EquipmentType - the Equipment Type that was just added
    """
    return equipment_service.add_equipment_type(subject, equipment_type)


@api.put("/modify-equipment-type", tags=["Admin Equipment Reservation System"])
def modify_equipment_type(
    equipment_type_details: TypeDetails,
    id: int,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentType:
    """
    Modifies an existing EquipmentType object

    Returns:
        EquipmentType - the Equipment Type that was just added
    """
    return equipment_service.modify_equipment_type(subject, id, equipment_type_details)


@api.delete("/delete-equipment-type", tags=["Admin Equipment Reservation System"])
def delete_equipment_type(
    equipment_type: EquipmentType,
    id: int,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentType:
    """
    Deletes an EquipmentType object from the system

    Returns:
        EquipmentType - the Equipment Type that was deleted
    """
    return equipment_service.delete_equipment_type(subject, id)
