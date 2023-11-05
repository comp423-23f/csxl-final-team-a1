from fastapi import APIRouter, Depends
from ..services.equipment import EquipmentService, EquipmentType, EquipmentItem

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
