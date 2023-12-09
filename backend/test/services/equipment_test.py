"""This file is used to test the EquipmentService functionality"""

from datetime import datetime, timedelta
import pytest
from unittest.mock import create_autospec

from ...models.equipment import EquipmentItem, EquipmentType, TypeDetails
from ...models.equipment.equipment_reservation import EquipmentReservation
from .fixtures import equipment_svc_integration, reservation_svc_integration
from ...services.equipment.equipment import EquipmentService
from ...services.equipment.reservation import ReservationService
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

valid_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now() + timedelta(days=3),
    return_description="",
)

invalid_user_mismatch_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=2,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now() + timedelta(days=3),
    return_description="",
)

invalid_excess_time_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now() + timedelta(days=6),
    return_description="",
)

invalid_past_checkout_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now() - timedelta(days=1),
    expected_return_date=datetime.now() + timedelta(days=1),
    return_description="",
)

invalid_item_id_new_reservation = EquipmentReservation(
    item_id=13424,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now() + timedelta(days=3),
    return_description="",
)

invalid_type_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=433434,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now() + timedelta(days=1),
    return_description="",
)

invalid_dates_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now() + timedelta(days=1),
    expected_return_date=datetime.now() - timedelta(days=1),
    return_description="",
)

invalid_hidden_item_new_reservation = EquipmentReservation(
    item_id=3,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now(),
    return_description="",
)

invalid_checked_out_new_reservation = EquipmentReservation(
    item_id=2,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now(),
    return_description="",
)

invalid_illegal_values_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=3,
    actual_return_date=datetime.now(),
    ambassador_check_out=True,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now() + timedelta(days=3),
    return_description="",
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
# add after reservations tests

# RESERVATIONS TESTS


# Test get_all_reservations()
def test_get_reservations_enforces_permissions(
    reservation_svc_integration: ReservationService,
):
    """Tests that permissions are enforced for get_reservations()"""
    # Setup to test permission enforcement on the PermissionService.
    reservation_svc_integration._permission_svc = create_autospec(
        reservation_svc_integration._permission_svc
    )

    # Assert that permission service is called with correct arguments and does not raise exception
    reservation_svc_integration.get_all_reservations(root)
    reservation_svc_integration._permission_svc.enforce.assert_called_with(
        root, "equipment.reservation", "equipment"
    )


def test_get_reservations_as_user(reservation_svc_integration: ReservationService):
    """Tests that all reservations CANNOT be retrieved as a base user"""
    with pytest.raises(UserPermissionException):
        reservation_svc_integration.get_all_reservations(user)
        pytest.fail()


def test_get_reservations_as_ambassador(
    reservation_svc_integration: ReservationService,
):
    """Tests that all reservations CAN be retrieved as an ambassador"""
    reserves = reservation_svc_integration.get_all_reservations(ambassador)
    assert len(reservations) == len(reserves)


# Test create_reservation()
def test_create_reservation_valid(reservation_svc_integration: ReservationService):
    """Tests that a valid reservation can be made as a base user"""
    reservation = reservation_svc_integration.create_reservation(
        valid_new_reservation, user
    )
    assert reservation is not None


def test_create_reservation_user_mismatch(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown when mismatch of user ids occurs"""
    with pytest.raises(PermissionError):
        reservation_svc_integration.create_reservation(
            invalid_user_mismatch_new_reservation, user
        )
        pytest.fail()


def test_create_reservation_excess_time(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown when time exceeds max"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_excess_time_new_reservation, user
        )
        pytest.fail()


def test_create_reservation_past_checkout(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown when checkout is in the past"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_past_checkout_new_reservation, user
        )
        pytest.fail()


def test_create_distant_return(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when expected return is over a week away"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_past_checkout_new_reservation, user
        )
        pytest.fail()


def test_create_quota_exceeded(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when user already has active reservation(s)"""
    with pytest.raises(Exception):
        # Can reuse this reservation because expected return date is now
        reservation_svc_integration.create_reservation(valid_new_reservation, user)
        reservation_svc_integration.create_reservation(valid_new_reservation, user)
        pytest.fail()


def test_create_nonexistent_type(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when given invalid type id"""
    with pytest.raises(ResourceNotFoundException):
        reservation_svc_integration.create_reservation(
            invalid_type_new_reservation, user
        )
        pytest.fail()


def test_create_nonexistent_item(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when given invalid item id on type"""
    with pytest.raises(ResourceNotFoundException):
        reservation_svc_integration.create_reservation(
            invalid_item_id_new_reservation, user
        )
        pytest.fail()


def test_create_checkout_after_return(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when given invalid item id on type"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_dates_new_reservation, user
        )
        pytest.fail()


def test_create_hidden_item(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when given hidden item id"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_hidden_item_new_reservation, user
        )
        pytest.fail()


def test_create_unavailable_item(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when given already checked out item id"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_checked_out_new_reservation, user
        )
        pytest.fail()


def test_create_illegal_values(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when given illegal values - set actual_return_date, ambassador_check_out or return_description"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_illegal_values_reservation, user
        )
        pytest.fail()


# Test find_available_item()


# Test get_active_reservations()
def test_get_active_reservations_enforces_permissions(
    reservation_svc_integration: ReservationService,
):
    """Tests that permissions are enforced for get_active_reservations()"""
    # Setup to test permission enforcement on the PermissionService.
    reservation_svc_integration._permission_svc = create_autospec(
        reservation_svc_integration._permission_svc
    )

    # Assert that permission service is called with correct arguments and does not raise exception
    reservation_svc_integration.get_active_reservations(ambassador)
    reservation_svc_integration._permission_svc.enforce.assert_called_with(
        ambassador, "equipment.reservation", "equipment"
    )


def test_get_active_reservations_as_ambassador(
    reservation_svc_integration: ReservationService,
):
    """Tests that ambassador can get active reservations"""
    reservations = reservation_svc_integration.get_active_reservations(ambassador)
    assert len(reservations) == 1
    assert reservations[0].item_id == 2
    assert reservations[0].ambassador_check_out == True
    assert reservations[0].actual_return_date is None


def test_get_active_reservations_as_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that user can't get active reservations"""
    with pytest.raises(UserPermissionException):
        reservation_svc_integration.get_active_reservations(user)
        pytest.fail()


# Test cancel_reservation()
def test_cancel_reservation_correct_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that ambassador can get active reservations"""
    reservation_svc_integration.cancel_reservation(3, root)
    assert len(reservation_svc_integration.get_all_reservations(ambassador)) == 2


def test_cancel_reservation_mismatch_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that PermissionError is thrown when wrong user cancels"""
    with pytest.raises(PermissionError):
        reservation_svc_integration.cancel_reservation(3, ambassador)
        pytest.fail()


def test_cancel_reservation_active(
    reservation_svc_integration: ReservationService,
):
    """Tests that returns False when attempting to cancel an active reservation"""
    assert reservation_svc_integration.cancel_reservation(2, root) == False


def test_cancel_reservation_nonexistent_id(
    reservation_svc_integration: ReservationService,
):
    """Tests that raises ResourceNotFoundException when attempting to cancel a nonexistent id"""
    with pytest.raises(ResourceNotFoundException):
        reservation_svc_integration.cancel_reservation(-1111111, root)
        pytest.fail()


# Test check_in_equipment()
def test_check_in_equipment_enforces_permissions(
    reservation_svc_integration: ReservationService,
):
    """Tests that permissions are enforced for check_in_equipment()"""
    # Setup to test permission enforcement on the PermissionService.
    reservation_svc_integration._permission_svc = create_autospec(
        reservation_svc_integration._permission_svc
    )

    # Assert that permission service is called with correct arguments and does not raise exception
    reservation_svc_integration.check_in_equipment(
        2, datetime.now(), "Fine", ambassador
    )
    reservation_svc_integration._permission_svc.enforce.assert_called_with(
        ambassador, "equipment.reservation", "equipment"
    )


def test_check_in_equipment_as_ambassador(
    reservation_svc_integration: ReservationService,
):
    """Tests that ambassador can checkin equipment"""
    time = datetime.now()
    reservation = reservation_svc_integration.check_in_equipment(
        2, time, "Fine", ambassador
    )
    assert reservation.ambassador_check_out == False
    assert reservation.actual_return_date == time
    assert reservation.return_description == "Fine"


def test_check_in_equipment_as_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that user cannot checkin equipment"""
    with pytest.raises(UserPermissionException):
        time = datetime.now()
        reservation_svc_integration.check_in_equipment(2, time, "Fine", user)
        pytest.fail()


def test_check_in_nonexistent_id(
    reservation_svc_integration: ReservationService,
):
    """Tests exception is thrown when given invalid ID"""
    with pytest.raises(ResourceNotFoundException):
        time = datetime.now()
        reservation_svc_integration.check_in_equipment(-1111, time, "Fine", ambassador)
        pytest.fail()


def test_check_in_invalid_return_date(
    reservation_svc_integration: ReservationService,
):
    """Tests exception is thrown when given invalid date"""
    with pytest.raises(Exception):
        time = datetime.now() - timedelta(days=5)
        reservation_svc_integration.check_in_equipment(2, time, "Fine", ambassador)
        pytest.fail()


# Test get_user_equipment_reservations()
def test_get_user_equipment_reservations_empty_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that no reservations are returned for a user with no reservations"""
    reservations = reservation_svc_integration.get_user_equipment_reservations(user)
    assert len(reservations) == 0


def test_get_user_equipment_reservations_nonempty_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that reservations are returned for a user with reservations"""
    reservations = reservation_svc_integration.get_user_equipment_reservations(root)
    assert len(reservations) == 3


# Test activate_reservation()
def test_activate_reservation_enforces_permissions(
    reservation_svc_integration: ReservationService,
):
    """Tests that permissions are enforced for activate_reservation()"""
    # Setup to test permission enforcement on the PermissionService.
    reservation_svc_integration._permission_svc = create_autospec(
        reservation_svc_integration._permission_svc
    )

    # Assert that permission service is called with correct arguments and does not raise exception
    reservation_svc_integration.activate_reservation(
        ambassador, 2
    )
    reservation_svc_integration._permission_svc.enforce.assert_called_with(
        ambassador, "equipment.reservation", "equipment"
    )


def test_activate_reservation_as_ambassador(
    reservation_svc_integration: ReservationService,
):
    """Tests that ambassador can activate reservation"""
    reservation = reservation_svc_integration.activate_reservation(ambassador,2)
    assert reservation.ambassador_check_out == True  

def test_activate_reservation_nonexistent_id(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown with invalid id"""
    with pytest.raises(ResourceNotFoundException):
        reservation_svc_integration.activate_reservation(ambassador,-1111)
        pytest.fail()


def test_activate_reservation_as_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown when a base user attempts"""
    with pytest.raises(UserPermissionException):
        reservation_svc_integration.activate_reservation(user,2)
        pytest.fail()


