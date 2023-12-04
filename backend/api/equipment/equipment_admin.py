from fastapi import APIRouter, Depends, HTTPException

from backend.models.user import User
from ..authentication import authenticated_pid, registered_user
from ...services.equipment.equipment import (
    EquipmentService,
    EquipmentType,
    EquipmentItem,
)
from ...services.exceptions import ResourceNotFoundException
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


@api.post("/create-type", tags=["Admin Equipment Reservation System"])
def create_type(
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
    Raises:
        HTTP Exception 422 if an exception was thrown in the service layer
    """
    try:
        return equipment_service.create_type(subject, equipment_type)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.put("/modify-type", tags=["Admin Equipment Reservation System"])
def modify_type(
    equipment_type: EquipmentType,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentType:
    """
    Modifies an existing EquipmentType object

    Parameters:
        equipment_type (EquipmentType): The new EquipmentType that will replace the old one
        subject (User): The user attempting the action
        equipment_service (EquipmentService): The Equipment backend service layer
    Returns:
        EquipmentType: The Equipment Type that was just added
    Raises:
        HTTP Exception 404 if the id was not found in the databse
        HTTP Exception 422 if the equipment_type was not well formed
    """
    try:
        return equipment_service.modify_type(subject, equipment_type)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.delete("/delete-type/{id}", tags=["Admin Equipment Reservation System"])
def delete_type(
    id: int,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentType:
    """
    Deletes an EquipmentType object from the system
    and all of it's associated EquipmentItems

    Parameters:
        id (int): The id of the EquipmentType to delete
        subject (User): The user attempting the action
        equipment_service (EquipmentService): The Equipment backend service layer
    Returns:
        EquipmentType: The Equipment Type that was deleted
    Raises:
        HTTP Exception 404 if the id was not found in the database
    """
    try:
        return equipment_service.delete_type(subject, id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post("/create-item/{type_id}", tags=["Admin Equipment Reservation System"])
def create_item(
    type_id: int,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentItem:
    """
    Creates a new EquipmentItem instance of type "type_id"

    Parameters:
        type_id (int): The id of the EquipmentType of the EquipmentItem
        subject (User): The user attempting the action
        equipment_service (EquipmentService): The equipment backend service layer
    Returns:
        EquipmentItem: The item that was created
    Raises:
        HTTP Exception 404 if the type_id was not found in the database
    """
    try:
        return equipment_service.create_item(subject, type_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.delete("/delete-item/{item_id}", tags=["Admin Equipment Reservation System"])
def delete_item(
    item_id: int,
    subject: User = Depends(registered_user),
    equipment_service: EquipmentService = Depends(),
) -> EquipmentItem:
    """
    Deletes an item in the databse

    Parameters:
        item_id (int): The id of the item to be deleted
        subject (User): The user attempting the action
        equipment_service (EquipmentService): The equipment service layer

    Returns:
        EquipmentItem: The item that was deleted
    Raises:
        HTTP Exception 404: if the id was not found in the databse
    """
    try:
        return equipment_service.delete_item(subject, item_id)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
