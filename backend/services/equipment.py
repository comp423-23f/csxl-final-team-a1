from fastapi import Depends
from sqlalchemy.orm import Session

from backend.services.permission import PermissionService
from ..database import db_session
from ..models.equipment.type_details import EquipmentType, TypeDetails
from ..models.equipment.item_details import EquipmentItem, ItemDetails


class EquipmentService:
    _session: Session

    equipments: list[EquipmentType] = [
        EquipmentType(
            id=0, title="Quest VR", description="blabla", max_reservation_time=3, img_url="https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6494/6494864_rd.jpg;maxHeight=640;maxWidth=550"
        ),
        EquipmentType(
            id=1, title="iPad", description="hihi", max_reservation_time=2, img_url="https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-10th-gen-finish-unselect-gallery-1-202212_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=95&.v=1667592096723"
        )
    ]
    items: list[ItemDetails] = [
        ItemDetails(id=0, equipment_type=equipments[0], display_status=True),
        ItemDetails(id=1, equipment_type=equipments[0], display_status=True),
        ItemDetails(id=2, equipment_type=equipments[0], display_status=False),
        ItemDetails(id=4, equipment_type=equipments[1], display_status=False)
    ]

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
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
