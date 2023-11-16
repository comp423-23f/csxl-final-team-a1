"""This file is used to test the EquipmentService functionality"""

import pytest

from ...models.equipment import EquipmentItem, EquipmentType, TypeDetails
from .fixtures import equipment_svc_integration
from ...services.equipment import EquipmentService
from .equipment_demo_data import (
    types,
    items,
    quest
)

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

def test_get_all_types(equipment_svc_integration: EquipmentService):
    """Test that all types can be retrieved"""
    fetched_types = equipment_svc_integration.get_all_types()
    assert fetched_types is not None
    assert len(fetched_types) == len(types)
    assert isinstance(fetched_types[0], EquipmentType)

def test_get_all(equipment_svc_integration: EquipmentService):
    """Test that get all can retreive all items in the types and items tables"""
    fetched: list[TypeDetails] = equipment_svc_integration.get_all()
    assert fetched is not None
    assert len(fetched) == len(types)
    s = 0
    for type_detail in fetched:
        s += len(type_detail.items)
    assert s == len(items)
    assert isinstance(fetched[0], TypeDetails)

def test_get_items_of_type(equipment_svc_integration: EquipmentService):
    fetched: list[EquipmentItem] = equipment_svc_integration.get_items_from_type(quest.id)
    assert fetched is not None
    assert len(fetched) == len([item for item in items if item.type_id==0])
    assert isinstance(fetched[0], EquipmentItem)
    for item in fetched:
        assert item.type_id == 0

# TODO: Finish Writing Tests
""" def test_create_type(equipment_svc_integration: EquipmentService):
    new_type = EquipmentType(
        id=None,
        title="iMom",
        img_url="",
        num_available=0,
        description="Need a mom?",
        max_reservation_time=3
    )
    equipment_svc_integration.create_type(new_type) """