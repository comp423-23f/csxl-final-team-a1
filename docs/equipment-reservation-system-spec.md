# Technical Specification Documentation - Equipment Reservation System

## Models

### Equipment Types

```py
class EquipmentType():
    id: int
    title: str
    img_url: str
    num_available: int
    description: str
    max_reservation_time: int
```

### Equipment Items

```py
class EquipmentItem():
    id: int
    type_id: int
    display_status: bool
```

## Design Choices

### User Experience
We opted for not offering an initial count option for admins when creating an equipment type.  We chose this over specifying how many items you want to create because we felt that it offered more flexibility to an admin, allowing them to create a type without automatically displaying new items to users.

## Development Concerns

### Frontend