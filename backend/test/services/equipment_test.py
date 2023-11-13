"""This file is used to test the EquipmentService functionality"""

import pytest

from ...models.equipment import EquipmentItem, EquipmentType
from .fixtures import equipment_svc_integration
from ...services.equipment import EquipmentService
from .equipment_demo_data import (
    types,
    items
)

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

def test_get_all_types(equipment_svc_integration: EquipmentService):
    """Test that all types can be retrieved"""
    fetched_types = equipment_svc_integration.get_all_types()
    assert fetched_types is not None
    assert len(fetched_types) == len(types)
    assert isinstance(fetched_types[0], EquipmentType)