"""This file is used to test the EquipmentService functionality"""

from datetime import datetime, timedelta
import pytest
from unittest.mock import create_autospec

from ...models.equipment import EquipmentItem, EquipmentType, TypeDetails
from ...models.equipment.equipment_reservation import EquipmentReservation
from ...entities.equipment.item_entity import EquipmentItemEntity
from .fixtures import equipment_svc_integration
from ...services.equipment.equipment import EquipmentService
from ...services.exceptions import UserPermissionException, ResourceNotFoundException
from .equipment_demo_data import types, items, quest, reservations

from .user_data import root, ambassador, user

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

new_type = EquipmentType(
    id=None,
    title="iMom",
    img_url="",
    num_available=0,
    description="Need a mom?",
    max_reservation_time=3,
)

modified_quest = EquipmentType(
    id=quest.id,
    title=quest.title,
    img_url="https://m.media-amazon.com/images/I/61EF6zFfLLL._AC_UF894,1000_QL80_.jpg",
    num_available=0,
    description="Quest 2 is actually really bad",
    max_reservation_time=quest.max_reservation_time,
)

# Test get_all_types()
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


# test get_items_of_type()
def test_get_items_of_type(equipment_svc_integration: EquipmentService):
    """Testing normal use case of get_items_from_type"""
    fetched: list[EquipmentItem] = equipment_svc_integration.get_items_from_type(
        quest.id
    )
    assert fetched is not None
    assert len(fetched) == len([item for item in items if item.type_id == quest.id])
    assert isinstance(fetched[0], EquipmentItem)
    for item in fetched:
        assert item.type_id == quest.id


def test_get_items_of_type_None(equipment_svc_integration: EquipmentService):
    """Testing when None or an out of bounds id is supplied"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.get_items_from_type(None)
        pytest.fail()

    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.get_items_from_type(700000)
        pytest.fail()


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
        pytest.fail()  # Fail if no error was thrown


def test_create_type_non_null_id(equipment_svc_integration: EquipmentService):
    """Tests that a non-null id can be created and will be ignored"""
    new_type = EquipmentType(
        id=12,
        title="iMom",
        img_url="",
        num_available=0,
        description="Need a mom?",
        max_reservation_time=3,
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
    equipment_svc_integration.modify_type(root, modified_quest)
    equipment_svc_integration._permission_svc.enforce.assert_called_with(
        root, "equipment.create", "equipment"
    )


def test_modify_type_as_root(equipment_svc_integration: EquipmentService):
    """Tests that the root user can modify equipment types"""
    modified = equipment_svc_integration.modify_type(root, modified_quest)
    assert modified is not None
    assert modified.title == modified_quest.title
    assert modified.img_url == modified_quest.img_url
    assert modified.description == modified_quest.description
    assert modified.max_reservation_time == modified_quest.max_reservation_time


def test_modify_type_as_user(equipment_svc_integration: EquipmentService):
    """Tests that users cannot modify equipment types"""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.modify_type(user, modified_quest)
        pytest.fail()


def test_modify_type_not_exist(equipment_svc_integration: EquipmentService):
    """Tests that the correct exception is thrown on incorrect params"""
    modified_quest.id = None
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.modify_type(root, modified_quest)
        pytest.fail()

    modified_quest.id = 7000000
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.modify_type(root, modified_quest)
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


def test_delete_type_not_valid(equipment_svc_integration: EquipmentService):
    """Tests delete_type with invalid id fields"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.delete_type(root, None)
        pytest.fail()

    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.delete_type(root, 70000)
        pytest.fail()


# Test create_item()
def test_create_item_as_root(equipment_svc_integration: EquipmentService):
    """Tests that create item works as expected when run as a root user"""
    items_before = equipment_svc_integration.get_items_from_type(quest.id)
    created = equipment_svc_integration.create_item(root, quest.id)
    items_after = equipment_svc_integration.get_items_from_type(quest.id)
    assert created is not None
    assert len(items_before) < len(items_after)
    assert created in items_after


def test_create_item_as_user(equipment_svc_integration: EquipmentService):
    """Tests that create item does not work when run as a user"""
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.create_item(user, quest.id)
        pytest.fail()


def test_create_item_invalid(equipment_svc_integration: EquipmentService):
    """Tests create_item using invalid type_id fields"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.create_item(root, None)
        pytest.fail()

    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.create_item(root, 700000)
        pytest.fail()


# Test update_item_availability()
def test_update_item_availability_enforces_perms(
    equipment_svc_integration: EquipmentService,
):
    """Tests that the update_item_availability requires the equipment.hide permission"""
    equipment_svc_integration._permission_svc = create_autospec(
        equipment_svc_integration._permission_svc
    )

    # Test permissions with root user
    equipment_svc_integration.update_item_availability(root, 1, False)
    equipment_svc_integration._permission_svc.enforce.assert_called_with(
        root, "equipment.hide", "equipment"
    )


def test_update_item_availability_as_root(equipment_svc_integration: EquipmentService):
    """Tests that update_item_availability works as expected for root user"""
    item = equipment_svc_integration.get_items_from_type(quest.id)[0]
    updated_item = equipment_svc_integration.update_item_availability(
        root, item.id, not item.display_status
    )
    assert updated_item is not None
    assert updated_item.display_status != item.display_status


def test_update_item_availability_as_user(equipment_svc_integration: EquipmentService):
    """Tests that update_item_availability does NOT run as a user"""
    item = equipment_svc_integration.get_items_from_type(quest.id)[0]
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.update_item_availability(user, item.id, True)
        pytest.fail()


def test_update_item_availbility_invalid(equipment_svc_integration: EquipmentService):
    """Tests update_item_availability with invalid parameters"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.update_item_availability(root, None, True)
        pytest.fail()

    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.update_item_availability(root, 700000, False)
        pytest.fail()


# Test delete_item()
def test_delete_item_as_root(equipment_svc_integration: EquipmentService):
    """Tests that delete item works as expected when run as root"""
    item_before = equipment_svc_integration.get_items_from_type(quest.id)
    deleted = equipment_svc_integration.delete_item(root, item_before[0].id)
    items_after = equipment_svc_integration.get_items_from_type(quest.id)
    assert deleted is not None
    assert len(item_before) > len(items_after)
    assert deleted not in items_after


def test_delete_item_as_user(equipment_svc_integration: EquipmentService):
    """Tests that delete item does not execute when run as a user"""
    items = equipment_svc_integration.get_items_from_type(quest.id)
    with pytest.raises(UserPermissionException):
        equipment_svc_integration.delete_item(user, items[0].id)
        pytest.fail()


def test_delete_item_invalid(equipment_svc_integration: EquipmentService):
    """Tests delete item when invalid id fields are passed"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.delete_item(root, None)
        pytest.fail()

    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.delete_item(root, 700000)
        pytest.fail()


# Test get_item_details_from_type()
def test_get_item_details_from_type_multiple_items(
    equipment_svc_integration: EquipmentService,
):
    """Tests that item details are returned"""
    item_details = equipment_svc_integration.get_item_details_from_type(1)
    assert len(item_details) == 3
    assert item_details[0].id == 1
    assert item_details[1].id == 2
    assert item_details[2].id == 3


def test_get_item_details_from_type_invalid_type(
    equipment_svc_integration: EquipmentService,
):
    """Tests that exception is thrown with invalid type id"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.get_item_details_from_type(-111)
        pytest.fail()


# Test get_availability() - Nested in to_details_model()
def test_get_availability_multiple_items(
    equipment_svc_integration: EquipmentService,
):
    """Tests that correct availability is returned for 3 items in a type"""
    availabilities = [equipment_svc_integration.get_availability(item) for item in range(1, 4)]
    assert list(availabilities[0].values()) == [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    ]
    assert list(availabilities[1].values()) == [
        False,
        False,
        True,
        True,
        True,
        True,
        True,
    ]
    assert list(availabilities[2].values()) == [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    ]


def test_get_availability_invalid_item_id(
    equipment_svc_integration: EquipmentService,
):
    """Tests that exception is raised when given invalid item id"""
    with pytest.raises(ResourceNotFoundException):
        equipment_svc_integration.get_availability(-1111)
        pytest.fail()