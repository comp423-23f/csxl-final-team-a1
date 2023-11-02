from fastapi import APIRouter, Depends
from ..services.equipment import EquipmentService, EquipmentType, EquipmentItem

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Equipment Reservation System",
    "description": "Reservation system that allow students to reserve lab-owned equipments for multiple days.",
}


@api.get("/list-all-equipment-availability", tags=["Equipment Reservation System"])
def list_all_equipment_availability(
    equipment_service: EquipmentService = Depends(),
) -> dict[EquipmentType, int]:
    return equipment_service.get_all_availability()
