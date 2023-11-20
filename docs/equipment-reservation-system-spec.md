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
```

```py
class ItemDetails(EquipmentItem):
    equipment_type: EquipmentType
```

The `EquipmentItem` model represents each individual item that is part of an `EquipmentType`. The integer `id` acts as a primary key for the database. `display_status` controls whether or not the item will be part of the available count displayed under each `EquipmentType` card on the equipment home page. Finally, the `type_id` relates the item back to its associated `EquipmentType` using the id of the type.

The `ItemDetails` model extends the `EquipmentItem` model with an `EquipmentType` field of the item's associated type.

#### Example:

```json
// ItemDetails JSON sample data
{
  "id": 3,
  "display_status": false,
  "type_id": 1,
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

## Design Choices

### Entity-Level: Extending `EquipmentType` and `EquipmentItem`

The `EquipmentType` and `EquipmentItem` classes were extended in order to avoid the problem of circular dependency. Both models need to have a connection to the other, but with just an attribute of the base class this leads to a an infinite recursive JSON representation, so the attributes were added to `TypeDetails` and `ItemDetails` classes that extended their respective bases classes.

### User Experience: Initial Item Count

We opted for not offering an initial count option for admins when creating an equipment type. We chose this over specifying how many items you want to create because we felt that it offered more flexibility to an admin, allowing them to create a type without automatically displaying new items to users.

### Technical: Equipment Usage Agreement

The original plan for the equipment agreement page was to have an API route that retrieved the text of the agreement from the backend and then to use that route to display the agreement to the user but ultimately we decided against it because we figured updates to the agreement would be rare. Instead, we went with a design similar to the existing "About the XL" page where the text is simply stored statically in the html file, where it can still be updated by changes to the codebase itself.

## Development Concerns

### Frontend

### Backend
