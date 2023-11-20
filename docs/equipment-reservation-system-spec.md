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

The `TypeDetails` model simply extends the `EquipmentType` model to include a list of all `EquipmentItem` objects associated with the type. This field is not included in the base class due to a circular relationship between the two types.

#### Example:

```json
{
  "id": 0,
  "title": "Quest VR",
  "img_url": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6494/6494864_rd.jpg;maxHeight=640;maxWidth=550",
  "num_available": 3,
  "description": "blabla",
  "max_reservation_time": 3,
  "items": [
    {
      "id": 0,
      "display_status": true,
      "type_id": 0
    },
    {
      "id": 1,
      "display_status": true,
      "type_id": 0
    },
    {
      "id": 2,
      "display_status": false,
      "type_id": 0
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

## Design Choices

### User Experience

We opted for not offering an initial count option for admins when creating an equipment type. We chose this over specifying how many items you want to create because we felt that it offered more flexibility to an admin, allowing them to create a type without automatically displaying new items to users.

## Development Concerns

### Frontend
