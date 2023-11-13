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