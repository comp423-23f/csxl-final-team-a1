from pydantic import BaseModel
from datetime import datetime

from ...models import User
from ...models.equipment import EquipmentItem, EquipmentType


class EquipmentReservation(BaseModel):
    """
    This model is used to track all reservations and returns

    This model will be used in conjunction with the
    EquipmentReservationEntity to store reservations in the
    database
    """

    id: int | None = None
    item_id: int
    type_id: int
    user_id: int
    check_out_date: datetime
    ambassador_check_out: bool  # active?
    expected_return_date: datetime
    actual_return_date: datetime | None
    return_description: str | None


class ReservationDetails(EquipmentReservation):
    """
    This details view includes the models for the item and user
    """

    item: EquipmentItem
    type: EquipmentType
    user: User
