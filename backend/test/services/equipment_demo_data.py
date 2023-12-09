"""Mock Data for Equipment Reservation System Demos"""


from datetime import datetime, timedelta
import pytest
from backend.entities.equipment.reservation_entity import EquipmentReservationEntity

from backend.models.equipment.equipment_reservation import EquipmentReservation
from ...models.equipment import EquipmentType, EquipmentItem
from sqlalchemy.orm import Session
from ...entities import EquipmentItemEntity, EquipmentTypeEntity
from .reset_table_id_seq import reset_table_id_seq

quest = EquipmentType(
    id=1,
    title="Quest VR",
    description="blabla",
    max_reservation_time=3,
    img_url="https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6494/6494864_rd.jpg;maxHeight=640;maxWidth=550",
)

ipad = EquipmentType(
    id=2,
    title="iPad",
    description="hihi",
    max_reservation_time=2,
    img_url="https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/ipad-10th-gen-finish-unselect-gallery-1-202212_FMT_WHH?wid=1280&hei=720&fmt=p-jpg&qlt=95&.v=1667592096723",
)

q1 = EquipmentItem(id=None, display_status=True, type_id=1)
q2 = EquipmentItem(id=None, display_status=True, type_id=1)
q3 = EquipmentItem(id=None, display_status=False, type_id=1)
i1 = EquipmentItem(id=None, display_status=False, type_id=2)

types = [quest, ipad]

items = [q1, q2, q3, i1]

reservations = [
    EquipmentReservation(
        item_id=1,
        type_id=1,
        user_id=1,
        check_out_date=datetime.now(),
        ambassador_check_out=True,
        expected_return_date=datetime.now(),
        actual_return_date=datetime.now(),
        return_description="",
    ),
    EquipmentReservation(
        item_id=2,
        type_id=1,
        user_id=1,
        check_out_date=datetime.now() - timedelta(days=1),
        ambassador_check_out=True,
        expected_return_date=datetime.now() + timedelta(days=1),
        actual_return_date=None,
        return_description="",
    ),
    EquipmentReservation(
        item_id=2,
        type_id=1,
        user_id=1,
        check_out_date=datetime.now() - timedelta(days=1),
        ambassador_check_out=False,
        expected_return_date=datetime.now() + timedelta(days=1),
        actual_return_date=None,
        return_description="",
    ),
]

# Data functions


def insert_fake_data(session: Session):
    """Inserts fake data for Equipment Types and Items"""
    global types, items

    for t in types:
        entity = EquipmentTypeEntity.from_model(t)
        session.add(entity)

    for item in items:
        entity = EquipmentItemEntity.from_model(item)
        session.add(entity)

    session.commit()

    for reservation in reservations:
        entity = EquipmentReservationEntity.from_model(reservation)
        session.add(entity)

    reset_table_id_seq(
        session, EquipmentTypeEntity, EquipmentTypeEntity.id, len(types) + 1
    )

    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
