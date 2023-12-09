"""This file is used to test the ReservationService functionality"""

from datetime import datetime, timedelta
import pytest
from unittest.mock import create_autospec

from ...models.equipment import EquipmentItem, EquipmentType, TypeDetails
from ...models.equipment.equipment_reservation import EquipmentReservation
from ...entities.equipment.item_entity import EquipmentItemEntity
from .fixtures import reservation_svc_integration
from ...services.equipment.reservation import ReservationService
from ...services.exceptions import UserPermissionException, ResourceNotFoundException
from .equipment_demo_data import types, items, quest, reservations

from .user_data import root, ambassador, user
from ...services.equipment.settings import MAX_RESERVATIONS, AVAILABILITY_DAYS

# Explicitly import Data Fixture to load entities in database
from .core_data import setup_insert_data_fixture

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

valid_new_reservation = EquipmentReservation(
    item_id=4,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now() + timedelta(days=3),
    return_description="",
)

valid_instant_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now(),
    expected_return_date=datetime.now(),
    return_description="",
)

invalid_unavailable_new_reservation = EquipmentReservation(
    item_id=2,
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

invalid_distant_checkout_new_reservation = EquipmentReservation(
    item_id=1,
    type_id=1,
    user_id=3,
    actual_return_date=None,
    ambassador_check_out=False,
    check_out_date=datetime.now() + timedelta(days=1),
    expected_return_date=datetime.now() + timedelta(days=AVAILABILITY_DAYS + 1),
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
    """Tests that exception is thrown when expected return date exceeds settings.AVAILABILITY_DAYS from now"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            invalid_distant_checkout_new_reservation, user
        )
        pytest.fail()


def test_create_quota_exceeded(reservation_svc_integration: ReservationService):
    """Tests that exception is thrown when user already has exceeded max reservations - assumes max reservations = 1"""
    with pytest.raises(Exception):
        reservation_svc_integration.create_reservation(
            valid_instant_new_reservation, user
        )
        reservation_svc_integration.create_reservation(valid_new_reservation, user)
        pytest.fail()


def test_create_quota_met(reservation_svc_integration: ReservationService):
    """Tests that no exception is thrown when user has max allowed reservations -- assumed to be 1"""
    reservation_svc_integration.create_reservation(valid_instant_new_reservation, user)


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
    """Tests that given illegal values are corrected"""
    reservation = reservation_svc_integration.create_reservation(
        invalid_illegal_values_reservation, user
    )
    assert reservation.actual_return_date == None
    assert reservation.ambassador_check_out == False
    assert reservation.return_description == ""


# Test find_available_item() - nested in create_reservation()
def test_find_available_item_available(
    reservation_svc_integration: ReservationService,
):
    """Tests that available item is marked as available"""
    assert (
        reservation_svc_integration.find_available_item(valid_new_reservation, 1) == 1
    )


def test_find_available_item_unavailable(
    reservation_svc_integration: ReservationService,
):
    """Tests that unavailable item is marked as unavailable"""
    with pytest.raises(Exception):
        assert (
            reservation_svc_integration.find_available_item(
                invalid_unavailable_new_reservation, 2
            )
            == 1
        )
        pytest.fail()


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
    reservation_svc_integration.activate_reservation(ambassador, 2)
    reservation_svc_integration._permission_svc.enforce.assert_called_with(
        ambassador, "equipment.reservation", "equipment"
    )


def test_activate_reservation_as_ambassador(
    reservation_svc_integration: ReservationService,
):
    """Tests that ambassador can activate reservation"""
    reservation = reservation_svc_integration.activate_reservation(ambassador, 2)
    assert reservation.ambassador_check_out == True


def test_activate_reservation_nonexistent_id(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown with invalid id"""
    with pytest.raises(ResourceNotFoundException):
        reservation_svc_integration.activate_reservation(ambassador, -1111)
        pytest.fail()


def test_activate_reservation_as_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown when a base user attempts"""
    with pytest.raises(UserPermissionException):
        reservation_svc_integration.activate_reservation(user, 2)
        pytest.fail()


# Test ambassador_cancel_reservation()
def test_ambassador_cancel_reservation_enforces_permissions(
    reservation_svc_integration: ReservationService,
):
    """Tests that permissions are enforced for ambassador_cancel_reservation()"""
    # Setup to test permission enforcement on the PermissionService.
    reservation_svc_integration._permission_svc = create_autospec(
        reservation_svc_integration._permission_svc
    )

    # Assert that permission service is called with correct arguments and does not raise exception
    reservation_svc_integration.ambassador_cancel_reservation(ambassador, 2)
    reservation_svc_integration._permission_svc.enforce.assert_called_with(
        ambassador, "equipment.reservation", "equipment"
    )


def test_ambassador_cancel_reservation_as_ambassador(
    reservation_svc_integration: ReservationService,
):
    """Tests that ambassador can cancel reservation"""
    reservation_svc_integration.ambassador_cancel_reservation(ambassador, 2)
    assert len(reservation_svc_integration.get_all_reservations(ambassador)) == 2


def test_ambassador_cancel_reservation_nonexistent_id(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown with invalid id"""
    with pytest.raises(ResourceNotFoundException):
        reservation_svc_integration.ambassador_cancel_reservation(ambassador, -1111)
        pytest.fail()


def test_ambassador_cancel_reservation_as_user(
    reservation_svc_integration: ReservationService,
):
    """Tests that exception is thrown when a base user attempts"""
    with pytest.raises(UserPermissionException):
        reservation_svc_integration.ambassador_cancel_reservation(user, 2)
        pytest.fail()
