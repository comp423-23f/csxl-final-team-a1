# Technical Specification Documentation - Equipment Reservation System

## Models

### **New Models**

### Equipment Types and Equipment Type Details

```py
class EquipmentType():
    id: int
    title: str
    img_url: str
    num_available: int
    description: str
    max_reservation_time: int
```

```py
class TypeDetails(EquipmentType):
    items: list[EquipmentItem]
```

The `EquipmentType` model represents an entire category of equipment such as iPads, iPhones, or keyboards. A unique integer id represents acts as the primary key for the model. The `title` is simply the name of the type of equipment, the `img_url` is for display on the home page, and `num_available` corresponds to the number of items associated with the type that are currently available. `max_reservation_time` is set to 3 by default.

The `TypeDetails` model simply extends the `EquipmentType` model to include a list of all `EquipmentItem` objects associated with the type.

#### Example:

```json
// TypeDetails JSON sample data
{
  "id": 1,
  "title": "Quest VR",
  "img_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6494/6494864_rd.jpg;maxHeight=640;maxWidth=550",
  "num_available": 2,
  "description": "Quest VR Immersive Headset",
  "max_reservation_time": 3,
  "items": [
    {
      "id": 1,
      "display_status": true,
      "type_id": 1
    },
    {
      "id": 2,
      "display_status": true,
      "type_id": 1
    },
    {
      "id": 3,
      "display_status": false,
      "type_id": 1
    }
  ]
}
```

### Equipment Items and Equipment Item Details

```py
class EquipmentItem():
    id: int
    type_id: int
    display_status: bool
    return_description: str
```

```py
class ItemDetails(EquipmentItem):
    equipment_type: EquipmentType
```

The `EquipmentItem` model represents each individual item that is part of an `EquipmentType`. The integer `id` acts as a primary key for the database. `display_status` controls whether or not the item will be part of the available count displayed under each `EquipmentType` card on the equipment home page. Finally, the `type_id` relates the item back to its associated `EquipmentType` using the id of the type. The `return_description` is used exclusively in the backend to compile reservation return descriptions.

The `ItemDetails` model extends the `EquipmentItem` model with an `EquipmentType` field of the item's associated type.

#### Example:

```json
// ItemDetails JSON sample data
{
  "id": 3,
  "display_status": false,
  "type_id": 1,
  "return_description": "Wed Dec 9 2023: None",
  "equipment_type": {
    "id": 1,
    "title": "Quest VR",
    "img_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6494/6494864_rd.jpg;maxHeight=640;maxWidth=550",
    "num_available": 3,
    "description": "Quest VR Immersive Headset",
    "max_reservation_time": 3
  }
}
```

### **Modified Models**

```py
class User():
    pid: int
    onyen: str
    first_name: str
    last_name: str
    email: str
    pronouns: str
    github: str
    github_id: int | None
    github_avatar: str | None
    agreement_status: bool # NEW!
```

The `User` model has been updated with one new field, `agreement_status` that tracks whether or not a user has agreed to the terms of service of equipment usage. By default it is set to false, and it is permanently set to true once the user agrees to the terms of service.

#### Example of a modified `User`:

```json
// User JSON sample data
{
  "id": 1,
  "pid": 999999999,
  "onyen": "root",
  "first_name": "Rhonda",
  "last_name": "Root",
  "email": "root@unc.edu",
  "pronouns": "She / Her / Hers",
  "github": "",
  "github_id": null,
  "github_avatar": null,
  "agreement_status": false, // NEW!
  "permissions": [
    {
      "id": 1,
      "action": "*",
      "resource": "*"
    }
  ]
}
```

### Equipment Reservation and Reservation Details

```py
class EquipmentReservation():
  id: int | None = None
  item_id: int
  type_id: int
  user_id: int
  check_out_date: datetime
  ambassador_check_out: bool  # active?
  expected_return_date: datetime
  actual_return_date: datetime | None
  return_description: str | None

class ReservationDetails(EquipmentReservation):
  item: EquipmentItem
  equipment_type: EquipmentType
  user: User
```

Example of an `EquipmentReservation`:

```json
// EquipmentReservation JSON sample data
{
  "id": 0,
  "item_id": 1,
  "type_id": 1,
  "user_id": 1,
  "check_out_date": "2023-01-01T03:02:18.545Z",
  "ambassador_check_out": false,
  "expected_return_date": "2023-01-03T03:02:18.545Z",
  "actual_return_date": "2023-01-03T03:02:18.545Z",
  "return_description": "Wed Dec 9 2023: Some description"
}
```

The `EquipmentReservation` model represents a reservation request made by a user. A unique integer id represents acts as the primary key for the model. `item_id` holds the id of a many-to-one relationship with `EquipmentItem`s, `type_id` holds the id of a many-to-one relationship with `EquipmentType`s, and `user_id` holds the id of a many-to-one relationship with `User`s. `checkout_date` contains the `datetime` object of the day the requesting user received the item. `expected_return_date` contains the day the user should return the object to the CSXL. The `actual_return_date` contains the day the user officially returned the item to the CSXL, and it should usually start as `None` if the return is not yet completed. The `return_desciprition` is a string that should be inputted by an ambassador or admin to describe the state of the returned item.

The `ReservationDetails` model relates the `item_id`, `type_id`, and `user_id` to `EquipmentItem`, `EquipmentType`, and `User` entities respectively.

## API Routes

### Equipment Reservation System

- `list-all-equipments`: Gets all `EquipmentType` models in the database
- `get-all`: Gets all `TypeDetails` models in the database
- `get-items-from-type`: Gets all `EquipmentItem` models associated with an id parameter
- `update-user-agreement-status`: Updates the `agreement_status` of the current `User` to be `True`
- `get-user-agreement-status`: Gets the current `agreement_status` of the current `User`
- `update-item`: Updates an `EquipmentItem` model's `display_status` to either `True` or `False`

### Admin Equipment Reservation System

- `create-type`: Creates a new `EquipmentType` in the database
- `modify-type`: Modifies an existing `EquipmentType` in the database
- `delete-type`: Deletes an `EquipmentType` from the database
- `create-item`: Creates an `EquipmentItem` associated with a certain `EquipmentType` using a `type_id`
- `delete-item`: Deletes an `EquipmentItem` associated with the `item_id` parameter

### Equipment Reservation Scheduling

- `get-reservations`: Gets all `ReservationDetails` from the database related to the `type_id` parameter.
- `create-reservation`: Creates a new `EquipmentReservation` according to the `reservation` parameter.
- `ambassador-get-all-reservations`: Gets all `ReservationDetails` in the database.
- `ambassador-get-active-reservations`: Gets all `ReservationDetails` that are checked out but not returned.
- `ambassador-cancel-reservation`: Deletes the `EquipmentReservation` by the `reservation_id` parameter.
- `cancel-reservation`: Deletes the reservation with id `reservation_id`.
- `check-in-equipment`: Modifies an `EquipmentReservation` by adding `return_date` and `description` where the id is `reservation_id`.
- `get-user-equipment-reservations`: Gets a `list[ReservationDetails]` of all the reservations made by the requesting user.
- `activate-reservation`: Updates an `EquipmentReservation` of id `reservation_id` to toggle the `ambassador_check_out` to true.

## Design Choices

### Entity-Level: Extending `EquipmentType`, `EquipmentItem`, and `EquipmentReservation`

The `EquipmentType`, `EquipmentItem`, and `EquipmentReservation` classes were extended in order to avoid the problem of circular dependency. All models need to have a connection to the other, but with just an attribute of the base class this leads to a an infinite recursive JSON representation, so the attributes were added to `TypeDetails`, `ItemDetails`, and `ReservationDetails` classes that extended their respective bases classes.

### User Experience: Initial Item Count

We opted for not offering an initial count option for admins when creating an equipment type. We chose this over specifying how many items you want to create because we felt that it offered more flexibility to an admin, allowing them to create a type without automatically displaying new items to users.

### Technical: Equipment Usage Agreement

The original plan for the equipment agreement page was to have an API route that retrieved the text of the agreement from the backend and then to use that route to display the agreement to the user but ultimately we decided against it because we figured updates to the agreement would be rare. Instead, we went with a design similar to the existing "About the XL" page where the text is simply stored statically in the html file, where it can still be updated by changes to the codebase itself.

## Development Concerns

### Frontend

All frontend components of the Equipment Reservation System can be found in the `frontend\src\app\equipment` or the `frontend\src\app\admin\equipment` directories.

#### Components/Widgets

**`frontend\src\app\equipment`**

- `agreement` component: This component is what users will see before agreeing to the terms of service when attempting to access the equipment home page.
- `equipment-display` component: This component is what users will see as the home page for the equipment reservation system. The display is made up of `equipment-card` widgets under headers for available and unavailable equipment.
- `equipment-card` widget: This widget displays the title, image, and number of available units (out of the total units) of equipment for each `EquipmentType`. This card is repeated for each type on the `equipment-display` component.

**`frontend\src\app\admin\equipment`**

- `admin-equipment-base` component: This component is the initial screen the admin user will see that displays all `EquipmentType` models in the database and options to create, modify, and delete.
- `admin-equipment-create` component: This component appears when the admin chooses to create a new equipment type, and the admin can enter values into a form to create a new `EquipmentType` and add it to the database.
- `admin-equipment-edit` component: This component appears when the admin chooses to modify an existing `EquipmentType` and the fields of the EquipmentType can be edited as well as the individual `EquipmentItem` models associated with the type.

#### Services

- `equipment` service: This service is found in `frontend\src\app\equipment` and calls the API routes located in `backend\api\equipment\equipment_reservation.py` to retrieve/update equipment data and agreement status's of users.
- `admin-equipment` service: This service is found in `frontend\src\app\admin\equipment` and calls the API routes found in `backend\api\equipment\equipment_admin.py` to allow the admin to create, edit, and delete `EquipmentType` and `EquipmentItem` models.

### Backend

#### API Routes

All API-related files can be found in `backend\api\equipment`

- `equipment_admin.py` contains all routes concerning the administrator's ability to edit the equipment database by creating, editing, and deleting `EquipmentType` and `EquipmentItem` models.
- `equipment_reservation_scheduling.py` contains all the routes concerning reservation views for all users.
- `equipment_reservation.py` contains all routes concerning the student view of the equipment home page and the agreement page.

#### Services

The backend equipment service is located in `backend\services\equipment.py` and controls all equipment-related services in the backend, and therefore is what all API routes use to retrieve and modify data.

The backend reservation service is located in `backend\services\reservation.py` and controls all reservation-related services in the backend, and therefore is what all API routes use to retrieve and modify data.

#### Entities

All entities are located in the `backend\entities\equipment` directory.

- `item_entity.py` contains the entity representing a single equipment item in the database. It has a relationship with the table for `EquipmentType` for its `eq_type` column.
- `type_entity.py` contains the entity representing an equipment type in the database. It has a relationship with the table for `EquipmentItem` for its `items` column.
- `reservation_entity.py` contains the entity representing an equipment reservation in the database. It has a relationship with the table for `EquipmentType`, `EquipmentItem`, and `User` for the `equipment_type`, `item`, and `user` columns respectively.
