from fastapi import APIRouter, Depends
from ..authentication import authenticated_pid
from ...services.equipment import EquipmentService, EquipmentType, EquipmentItem
from ...models.equipment.equipment_type import EquipmentType
from ...models.equipment.equipment_item import EquipmentItem
from ...models.equipment.item_details import ItemDetails
from ...models.equipment.type_details import TypeDetails

api = APIRouter(prefix="/api/equipment/admin")
openapi_tags = {
    "name": "Equipment Reservation System Admin",
    "description": "Admin-only system for adding, modifying, and deleting equipment from the system.",
}

@api.post("/add-equipment-type", tags=["Equipment Reservation System Admin"])
def add_equipment_type(equipment_type: EquipmentType, pid_onyen: tuple[int, str] = Depends(authenticated_pid)) -> TypeDetails:
    """
    Adds a new EquipmentType to the system

    Returns:
        EquipmentType - the Equipment Type that was just added
    """
    ...


@api.put("/modify-equipment-type", tags=["Equipment Reservation System Admin"])
def modify_equipment_type(equipment_type: EquipmentType, pid_onyen: tuple[int, str] = Depends(authenticated_pid)) -> EquipmentType:
    """
    Modifies an existing EquipmentType object

    Returns:
        EquipmentType - the Equipment Type that was just added
    """
    ...

@api.delete("/delete-equipment-type", tags=["Equipment Reservation System Admin"])
def delete_equipment_type(equipment_type: EquipmentType, pid_onyen: tuple[int, str] = Depends(authenticated_pid)) -> EquipmentType:
    """
    Deletes an EquipmentType object from the system

    Returns:
        EquipmentType - the Equipment Type that was deleted
    """
    ...