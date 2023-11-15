"""
The EquipmentService allows the API to manipulate equipment related data in the database
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

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
        permission: PermissionService = Depends(),
    ):
        """Initialize the User Service."""
        self._session = session
        self._permission = permission

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
    
    def create_type(self, subject: User, new_type: EquipmentType) -> EquipmentType:
        """
        Adds a new type to the database if the id is unique
        Otherwise an error is returned

        Parameters:
            subject: User currenlty logged in
            new_type: EquipmentType to add to the database
        
        Returns:
            EquipmentType: Type added to the databse
        """
        self._permission.enforce(subject, "equipment.create_type", "equipment")

        entity = EquipmentTypeEntity.from_model(new_type)
        self._session.add(entity)
        self._session.commit()

        return entity.to_model()

    # TODO: Add test for create_type
