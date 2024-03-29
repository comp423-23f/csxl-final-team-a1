"""
The EquipmentService allows the API to manipulate equipment related data in the database
"""

from typing import Dict
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.services.exceptions import ResourceNotFoundException

from backend.services.permission import PermissionService
from ...database import db_session
from ...models.equipment.type_details import EquipmentType, TypeDetails
from ...models.equipment.item_details import EquipmentItem, ItemDetails
from ...entities import EquipmentItemEntity, EquipmentTypeEntity
from ...entities.equipment.reservation_entity import EquipmentReservationEntity
from ...models import User
from .settings import MAX_RESERVATIONS, AVAILABILITY_DAYS

from datetime import datetime, timedelta


class EquipmentService:
    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initialize the User Service."""
        self._session = session
        self._permission_svc = permission_svc

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

    def get_items_from_type(self, type_id: None | int) -> list[EquipmentItem]:
        """
        Retrievies all items of a specific type

        Parameters:
            eq_type: EquipmentType - Type of items to retreive

        Returns:
            list[EquipmentItems] - items of the specified type

        Raises:
            ResourceNotFoundException - thrown if the id is not valid
        """
        if (
            type_id == None
            or type_id < 0
            or type_id > self._session.query(EquipmentTypeEntity).count()
        ):
            raise ResourceNotFoundException("type_id field was not valid")

        entity = self._session.get(EquipmentTypeEntity, type_id)
        return entity.to_details_model().items

    def get_item_details_from_type(self, type_id: int) -> list[ItemDetails]:
        """
        Retrievies all item details of a specific type

        Parameters:
            eq_type: EquipmentType - Type of item details to retreive

        Returns:
            list[ItemDetails] - item details of the specified type

        Raises:
            ResourceNotFoundException - thrown if the id is not valid
        """
        query = select(EquipmentTypeEntity).where(EquipmentTypeEntity.id == type_id)
        entity = self._session.scalars(query).first()

        if entity is None:
            raise ResourceNotFoundException("No such type")

        query = select(EquipmentItemEntity).where(
            EquipmentItemEntity.type_id == type_id
        )
        entities = self._session.scalars(query).all()

        return [self.to_details_model(entity) for entity in entities]

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
        self._permission_svc.enforce(subject, "equipment.create", "equipment")

        if equipment_type.id != None:
            equipment_type.id = None

        entity = EquipmentTypeEntity.from_model(equipment_type)
        self._session.add(entity)
        self._session.commit()
        return entity.to_model()

    def modify_type(
        self, subject: User, equipment_type: EquipmentType
    ) -> EquipmentType:
        """
        Modify an existing equipment type in the database

        Args:
            subject (User): The User attempting the action
            id (int): The id of the EquipmentType to be modified
            equipment_type (EquipmentType): The equipment type that the old one will be updated to
        Returns:
            EquipmentType: The EquipmentType that was just modified
        Throws:
            ResourceNotFoundException: Thrown if the id cannot be found in the database
        """
        self._permission_svc.enforce(subject, "equipment.create", "equipment")
        if equipment_type.id == None:
            raise ResourceNotFoundException("Cannot find null id type")
        entity = self._session.get(EquipmentTypeEntity, equipment_type.id)
        if entity is None:
            raise ResourceNotFoundException(
                f"Equipment(id={equipment_type.id}) does not exist"
            )
        entity.title = equipment_type.title
        entity.img_url = equipment_type.img_url
        entity.desc = equipment_type.description
        entity.max_time = equipment_type.max_reservation_time

        self._session.commit()
        return entity.to_model()

    def delete_type(self, subject: User, id: int | None) -> TypeDetails:
        """
        Delete an equipment type and all it's associated items from the database

        Args:
            subject (User): The User attempting the action
            id (int): The id of the EquipmentType to be deleted
        Returns:
            EquipmentDetails: The EquipmentType details view that was just deleted
        Throws:
            ResourceNotFoundException: Thrown if the id cannot be found in the database
        """
        self._permission_svc.enforce(subject, "equipment.create", "equipment")
        if id is None:
            raise ResourceNotFoundException("Cannot delete type of Null id")
        entity = self._session.get(EquipmentTypeEntity, id)

        if entity is None:
            raise ResourceNotFoundException(f"Equipment(id={id}) does not exist")

        # Delete all items of type
        for item in entity.items:
            # Find reservations with deleted item
            query = select(EquipmentReservationEntity).where(
                EquipmentReservationEntity.item_id == item.id
            )
            reservation_entities = self._session.scalars(query).all()

            # Delete reservation entities
            for reservation in reservation_entities:
                self._session.delete(reservation)

            self.delete_item(subject, item.id)

        self._session.delete(entity)
        self._session.commit()
        return entity.to_details_model()

    def create_item(self, subject: User, type_id: int | None) -> EquipmentItem:
        """
        Creates an EquipmentItem of equipment type `type_id`

        Args:
            subject (User): The User attempting the action
            type_id (int): The id of the equipmentType of the new item

        Returns:
            EquipmentItem: The Item just created
        Throws:
            ResourceNotFoundException: If the id cannot be found in the database
        """
        self._permission_svc.enforce(subject, "equipment.create", "equipment")

        if type_id is None:
            raise ResourceNotFoundException("Cannot find type of Null id")

        type_entity = self._session.get(EquipmentTypeEntity, type_id)
        if type_entity is None:
            raise ResourceNotFoundException(
                f"EquipmentType (id = {type_id}) does not exist"
            )

        new_item = EquipmentItem(id=None, display_status=True, type_id=type_entity.id)
        item_entity = EquipmentItemEntity.from_model(new_item)
        self._session.add(item_entity)
        self._session.commit()
        return item_entity.to_model()

    def update_item_availability(
        self, subject: User, item_id: int | None, available: bool
    ) -> EquipmentItem:
        """
        Sets the item specified by item_id's display status to `available`
        NOTE: Requires equipment.hide permission

        Parameters:
            Subject (User): The user attempting the action
            item_id (int): The id of the item to change display status of
            available (bool): T/F whether to set the item to display or not

        Returns:
            EquipmentItem: Updated EquipmentItem

        Throws:
            ResourceNotFoundException: If the item_id was not found
        """
        self._permission_svc.enforce(subject, "equipment.hide", "equipment")

        if item_id is None:
            raise ResourceNotFoundException("Cannot find a null item!")

        entity = self._session.get(EquipmentItemEntity, item_id)

        if entity is None:
            raise ResourceNotFoundException(f"Cannot find item with id = {item_id}")

        entity.display_status = available

        self._session.commit()
        return entity.to_model()

    def delete_item(self, subject: User, item_id: int | None) -> EquipmentItem:
        """
        Deletes an equipment item in the database

        Args:
            subject (User): The User attempting the action
            item_id (int): The id of the item to be removed

        Returns:
            EquipmentItem: The item removed
        Throws:
            ResourceNotFoundException: If the id cannot be found in the database
        """
        self._permission_svc.enforce(subject, "equipment.create", "equipment")

        if item_id is None:
            raise ResourceNotFoundException("Cannot find type of null id")

        entity = self._session.get(EquipmentItemEntity, item_id)
        if entity is None:
            raise ResourceNotFoundException(f"Item of id={item_id} does not exist")

        # Find reservations with deleted item
        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.item_id == item_id
        )
        reservation_entities = self._session.scalars(query).all()

        # Delete reservation entities
        for reservation in reservation_entities:
            self._session.delete(reservation)

        self._session.delete(entity)
        self._session.commit()
        return entity.to_model()

    def get_availability(self, item_id: int) -> Dict[str, bool]:
        """
        Returns availability given an item_id

        Parameters:
            item_id: int

        Returns:
            Dict[str, bool]: availability for next AVAILABILITY_DAYS days

        Raises:
            ResourceNotFoundException - if no such item
        """
        times = [datetime.now() + timedelta(days=i) for i in range(AVAILABILITY_DAYS)]

        query = select(EquipmentItemEntity).where(EquipmentItemEntity.id == item_id)
        entity = self._session.scalars(query).first()

        if entity is None:
            raise ResourceNotFoundException("No such item")

        # Query all active reservations for the item
        query = (
            select(EquipmentReservationEntity)
            .where(EquipmentReservationEntity.item_id == item_id)
            .where(EquipmentReservationEntity.actual_return_date == None)
        )
        entities = self._session.scalars(query).all()

        # Check to see if each time is included in the range of any queried reservation
        availability = {}
        for time in times:
            availability[time.strftime("%Y-%m-%d")] = True
            for entity in entities:
                if (
                    entity.check_out_date.date()
                    <= time.date()
                    <= entity.expected_return_date.date()
                ):
                    availability[time.strftime("%Y-%m-%d")] = False
                    break

        return availability

    # Here to avoid circular dependencies
    def to_details_model(self, item: EquipmentItemEntity) -> ItemDetails:
        """
        Converts an EquipmentItemEntity into a ItemDetails model

        Returns:
            ItemDetails: Details model of entity
        """
        return ItemDetails(
            id=item.id,
            display_status=item.display_status,
            type_id=item.type_id,
            availability=self.get_availability(item.id),
            equipment_type=item.eq_type.to_model(),
        )
