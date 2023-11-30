from .equipment_item import EquipmentItem
from .equipment_type import EquipmentType
from typing import Dict

class ItemDetails(EquipmentItem):
    """Storing Equipment Type for the Item"""
    
    equipment_type: EquipmentType
    availability: Dict[str, bool]
    