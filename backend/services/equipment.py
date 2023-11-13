"""
The EquipmentService allows the API to manipulate equipment related data in the database
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.equipment.type_details import EquipmentType, TypeDetails
from ..models.equipment.item_details import EquipmentItem, ItemDetails
from ..entities import EquipmentItemEntity, EquipmentTypeEntity


class EquipmentService:

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initialize the User Service."""
        self._session = session

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

    # TODO: Add tests for these methods

    # def get_items_by_type(self, availability: bool) -> list[EquipmentItem]:
    #     """Return all unique items filtered by their type and availability."""
