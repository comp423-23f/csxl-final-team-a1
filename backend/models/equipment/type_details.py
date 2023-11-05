from .equipment_type import EquipmentType
from .equipment_item import EquipmentItem

class TypeDetails(EquipmentType):
    """Adding Items to their respective types"""
    items: list[EquipmentItem]
