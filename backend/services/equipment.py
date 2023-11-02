from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import db_session
from ..models.equipment_type import EquipmentType
from ..models.equipment_item import EquipmentItem


class EquipmentService:
    _session: Session

    equipments: list[EquipmentType] = [
        EquipmentType(
            id=0, title="Quest VR", description="blabla", max_reservation_time=3
        )
    ]
    items: list[EquipmentItem] = [
        EquipmentItem(id=0, equipment_type=equipments[0], display_status=True),
        EquipmentItem(id=1, equipment_type=equipments[0], display_status=True),
        EquipmentItem(id=2, equipment_type=equipments[0], display_status=False),
    ]

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initialize the User Service."""
        self._session = session

    def get_all_types(self) -> list[EquipmentType]:
        """Returns list item types."""
        return self.equipments

    def get_all_availability(self) -> dict[EquipmentType, int]:
        """Return dictionary relating EquipmentType to the number of available items."""
        eqs: dict[EquipmentType, int] = {equipment: 0 for equipment in self.equipments}
        for item in self.items:
            if item.display_status:
                eqs[item.equipment_type] += 1

        return eqs

    # def get_items_by_type(self, availability: bool) -> list[EquipmentItem]:
    #     """Return all unique items filtered by their type and availability."""
