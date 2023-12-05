import EquipmentType from './type.model';

export default interface ItemDetails {
  id: number;
  display_status: Boolean;
  equipment_type: EquipmentType;
  availability: { [date: string]: boolean };
}
