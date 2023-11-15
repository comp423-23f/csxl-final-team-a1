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
from ..models import User


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

    def create_type(
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
            subject, "equipment.create", "equipment"
        )
        entity = EquipmentTypeEntity.from_model(equipment_type)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def modify_type(
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
            subject, "equipment.create", "equipment"
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

    def delete_type(self, subject: User, id: int) -> TypeDetails:
        """
        Delete an equipment type from the database

        Args:
            subject (User): The User attempting the action
            id (int): The id of the EquipmentType to be deleted
        Returns:
            EquipmentType: The EquipmentType that was just deleted
        """
        self._permission_svc.enforce(
            subject, "equipment.create", "equipment"
        )
        entity = self._session.get(EquipmentTypeEntity, id)
        if entity is None:
            raise ResourceNotFoundException(f"Equipment(id={id}) does not exist")
        self._session.delete(entity)
        self._session.flush()
        self._session.commit()
        return entity.to_details_model()

    # TODO: Add tests for these methods

    def get_all(self) -> list[TypeDetails]:
        """
        Retrieves all TypeDetails views from the database

        Returns:
            list[TypeDetails]: List of all EquipmentTypes and associated EquipmentItems
        """

        # Select all entries in the 'equipment-type' table
        query = select(EquipmentTypeEntity)
        entities = self._session.scalars(query).all()

        # Convert entries to a model and return

        return [entity.to_details_model() for entity in entities]
    
    def get_items_from_type(self, type_id: int | None) -> list[EquipmentItem]:
        """
        Retrievies all items of a specific type

        Parameters:
            eq_type: EquipmentType - Type of items to retreive
        
        Returns:
            list[EquipmentItems] - items of the specified type
        
        Raises:
            ValueError - thrown if the id is not valid
        """
        if type_id < 0 or type_id > self._session.query(EquipmentTypeEntity).count():
            raise ValueError("type_id field was not valid")
        
        entity = self._session.get(EquipmentTypeEntity, type_id)
        return entity.to_details_model().items
    
