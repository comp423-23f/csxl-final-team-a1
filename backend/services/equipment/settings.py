# This file will be used for setting parameters: the maximum active reservations a user can have at a time and how many upcoming days availability is assessed for each item
# It is read and used by EquipmentService and ReservationService and in their respective tests

# Must be int, >= 0
MAX_RESERVATIONS = 1

# Must be int, >= 0
AVAILABILITY_DAYS = 10