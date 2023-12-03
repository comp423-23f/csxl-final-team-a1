"""
The Reservation Service allows the API to manipulate equipment reservation related data in the database
"""


from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.entities.equipment.reservation_entity import EquipmentReservationEntity
from backend.models.equipment.equipment_reservation import EquipmentReservation
from backend.models.user import User
from backend.services.exceptions import ResourceNotFoundException

from backend.services.permission import PermissionService
from ...database import db_session
from ...models.equipment.type_details import EquipmentType, TypeDetails
from ...models.equipment.item_details import EquipmentItem, ItemDetails
from ...entities import EquipmentItemEntity, EquipmentTypeEntity
from ...models import User


class ReservationService:
    def __init__(
        self,
        session: Session = Depends(db_session),
        permission_svc: PermissionService = Depends(),
    ):
        """Initialize the Reservation Service."""
        self._session = session
        self._permission_svc = permission_svc

    def get_reservations(self, type_id: int) -> list[EquipmentReservation]:
        """
        Retrieves all reservations of specified type.

        Parameters:
            type_id: id of the type to retrieve items of

        Returns:
            list[EquipmentReservation]: list of reservations of the supplied type
        """
        query = select(EquipmentReservationEntity).where(
            EquipmentReservationEntity.type_id == type_id
        )
        entities = self._session.scalars(query).all()

        return [entity.to_details_model() for entity in entities]
