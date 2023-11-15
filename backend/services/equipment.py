"""
The EquipmentService allows the API to manipulate equipment related data in the database
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.services.exceptions import ResourceNotFoundException

from backend.services.permission import PermissionService
from ..database import db_session
from ..models.equipment.type_details import EquipmentType, TypeDetails
from ..models.equipment.item_details import EquipmentItem, ItemDetails
from ..entities import EquipmentItemEntity, EquipmentTypeEntity


class EquipmentService:
    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initialize the User Service."""
        self._session = session
        self._permission_svc = permission_svc

    def get_all_types(self) -> list[EquipmentType]:
        """
        Retrieves all equipment types from the database

        Returns:
            list[EquipmentType]: List of all equipment types in the database
        """
        # Select all entries in the 'equipment-type' table
        query = select(EquipmentTypeEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return

        return [entity.to_model() for entity in entities]

    def add_equipment_type(
        self, subject: User, equipment_type: EquipmentType
    ) -> EquipmentType:
        """
        Add an equipment type to the database

        Args:
            subject (User): The User attempting the action
            equipment_type (EquipmentType): The equipment type that will be added
        Returns:
            EquipmentType: The EquipmentType that was just added
        """
        self._permission_svc.enforce(
            subject, "equipment.add-equipment-type", "equipment"
        )
        entity = EquipmentTypeEntity.from_model(equipment_type)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def modify_equipment_type(
        self, subject: User, id: int, equipment_type: EquipmentType
    ) -> EquipmentType:
        """
        Modify an existing equipment type in the database

        Args:
            subject (User): The User attempting the action
            id (int): The id of the EquipmentType to be modified
            equipment_type (EquipmentType): The equipment type that the old one will be updated to
        Returns:
            EquipmentType: The EquipmentType that was just modified
        """
        # TODO : Add a get route for use in the frontend to let frontend be able to have the id
        self._permission_svc.enforce(
            subject, "equipment.add-equipment-type", "equipment"
        )
        entity = self._session.get(EquipmentTypeEntity, id)
        if entity is None:
            raise ResourceNotFoundException(f"Equipment(id={id}) does not exist")
        entity.title = equipment_type.title
        entity.img_url = equipment_type.img_url
        entity.desc = equipment_type.description
        entity.max_time = equipment_type.max_reservation_time

        self._session.flush()
        self._session.commit()
        return entity.to_model()

    def delete_equipment_type(self, subject: User, id: int) -> TypeDetails:
        """
        Delete an equipment type from the database

        Args:
            subject (User): The User attempting the action
            id (int): The id of the EquipmentType to be deleted
        Returns:
            EquipmentType: The EquipmentType that was just deleted
        """
        self._permission_svc.enforce(
            subject, "equipment.add-equipment-type", "equipment"
        )
        entity = self._session.get(EquipmentTypeEntity, id)
        if entity is None:
            raise ResourceNotFoundException(f"Equipment(id={id}) does not exist")
        self._session.delete(entity)
        self._session.flush()
        self._session.commit()
        return entity.to_details_model()

    # TODO: Add tests for these methods

    # def get_items_by_type(self, availability: bool) -> list[EquipmentItem]:
    #     """Return all unique items filtered by their type and availability."""
