from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import db_session
from ..models.equipment.type_details import EquipmentType, TypeDetails
from ..models.equipment.item_details import EquipmentItem, ItemDetails


class EquipmentService:
    _session: Session

    equipments: list[EquipmentType] = [
        EquipmentType(
            id=0, title="Quest VR", description="blabla", max_reservation_time=3
        )
    ]
    items: list[ItemDetails] = [
        ItemDetails(id=0, equipment_type=equipments[0], display_status=True),
        ItemDetails(id=1, equipment_type=equipments[0], display_status=True),
        ItemDetails(id=2, equipment_type=equipments[0], display_status=False),
    ]

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initialize the User Service."""
        self._session = session

    def get_all_types(self) -> list[EquipmentType]:
        """Returns list item types."""
        self.update_all_availability()

        return self.equipments

    def update_all_availability(self):
        """Return dictionary relating EquipmentType to the number of available items."""
        for eq in self.equipments:
            eq.num_available = 0

        for item in self.items:
            if item.display_status:
                item.equipment_type.num_available += 1

    # TODO: Add tests for these 2 methods

    # def get_items_by_type(self, availability: bool) -> list[EquipmentItem]:
    #     """Return all unique items filtered by their type and availability."""
