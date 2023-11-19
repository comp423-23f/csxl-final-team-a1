"""This file is used to test the EquipmentService functionality"""

import pytest
from unittest.mock import create_autospec

from ...models.equipment import EquipmentItem, EquipmentType, TypeDetails
from .fixtures import equipment_svc_integration
from ...services.equipment import EquipmentService
from ...services.exceptions import UserPermissionException, ResourceNotFoundException
from .equipment_demo_data import (
    types,
    items,
    quest
)

from .user_data import root, ambassador, user

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

new_type = EquipmentType(
    id=None,
    title="iMom",
    img_url="",
    num_available=0,
    description="Need a mom?",
    max_reservation_time=3
)

modified_quest = EquipmentType(
    id=quest.id,
    title=quest.title,
    img_url="https://m.media-amazon.com/images/I/61EF6zFfLLL._AC_UF894,1000_QL80_.jpg",
    num_available=0,
    description="Quest 2 is actually really bad",
    max_reservation_time=quest.max_reservation_time
)

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
    assert len(fetched) == len([item for item in items if item.type_id==quest.id])
    assert isinstance(fetched[0], EquipmentItem)
    for item in fetched:
        assert item.type_id == quest.id

# Test create_type()
def test_create_type_enforces_permissions(equipment_svc_integration: EquipmentService):
    """Test that the service class is enforcing permissions when attempting to create an Euqipment Type"""
    # Setup to test permission enforcement
    equipment_svc_integration._permission_svc = create_autospec(
        equipment_svc_integration._permission_svc
    )

    # Test permissions with root user
    equipment_svc_integration.create_type(root, new_type)
    equipment_svc_integration._permission_svc.enforce.assert_called_with(
        root, "equipment.create", "equipment"
    )

def test_create_type_as_root(equipment_svc_integration: EquipmentService):
    """Tests that root user is able to create new equipment types"""
    created = equipment_svc_integration.create_type(root, new_type)
    assert created is not None
    assert created.id is not None
    assert created.id == types[-1].id + 1

def test_create_type_as_user(equipment_svc_integration: EquipmentService):
    """Tests that any user can NOT create new equipment types"""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.create_type(user, new_type)
        pytest.fail() # Fail if no error was thrown

def test_create_type_non_null_id(equipment_svc_integration: EquipmentService):
    """Tests that a non-null id can be created and will be ignored"""
    new_type =  EquipmentType(
        id=12,
        title="iMom",
        img_url="",
        num_available=0,
        description="Need a mom?",
        max_reservation_time=3
    )
    created = equipment_svc_integration.create_type(root, new_type)
    assert created is not None
    assert created.id == types[-1].id + 1

# Test modify_type()
def test_modify_type_enforces_permission(equipment_svc_integration: EquipmentService):
    """Tests that modify_type() checks for permissions"""
    # Setup to test permission enforcement
    equipment_svc_integration._permission_svc = create_autospec(
        equipment_svc_integration._permission_svc
    )

    # Test permissions with root user
    equipment_svc_integration.modify_type(root, quest.id, modified_quest)
    equipment_svc_integration._permission_svc.enforce.assert_called_with(
        root, "equipment.create", "equipment"
    )

def test_modify_type_as_root(equipment_svc_integration: EquipmentService):
    """Tests that the root user can modify equipment types"""
    modified = equipment_svc_integration.modify_type(root, quest.id, modified_quest)
    assert modified is not None
    assert modified.title == modified_quest.title
    assert modified.img_url == modified_quest.img_url
    assert modified.description == modified_quest.description
    assert modified.max_reservation_time == modified_quest.max_reservation_time

def test_modify_type_as_user(equipment_svc_integration: EquipmentService):
    """Tests that users cannot modify equipment types"""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.modify_type(user, quest.id, modified_quest)
        pytest.fail()

def test_modify_type_not_exist(equipment_svc_integration: EquipmentService):
    """Tests that the correct exception is thrown on incorrect params"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.modify_type(root, None, modified_quest)
        pytest.fail()
    
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.modify_type(root, types[-1].id + 1000, modified_quest)
        pytest.fail()

# Test delete_type()
def test_delete_type_enforces_perms(equipment_svc_integration: EquipmentService):
    """Tests that delete_type() enforces permissions"""
    equipment_svc_integration._permission_svc = create_autospec(
        equipment_svc_integration._permission_svc
    )

    # Test permissions with root user
    equipment_svc_integration.delete_type(root, quest.id)
    equipment_svc_integration._permission_svc.enforce.assert_called_with(
        root, "equipment.create", "equipment"
    )

def test_delete_type_as_root(equipment_svc_integration: EquipmentService):
    """Tests that delete type works as expected as a root user"""
    deleted = equipment_svc_integration.delete_type(root, quest.id)
    assert deleted is not None
    rest = equipment_svc_integration.get_all()
    for t in rest:
        assert t.title != deleted.title

def test_delete_type_as_user(equipment_svc_integration: EquipmentService):
    """Tests that delete type does not run when exectued as a User"""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.delete_type(user, quest.id)
        pytest.fail()
