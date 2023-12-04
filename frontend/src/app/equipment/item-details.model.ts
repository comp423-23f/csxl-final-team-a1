import EquipmentType from './type.model';

export default interface ItemDetails {
  id: Number | null;
  display_status: Boolean;
  equipment_type: EquipmentType;
  availability: { [date: string]: boolean };
}
