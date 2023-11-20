import EquipmentItem from './equipment-item.model';

//This model aligns with the backends Pydantic TypeDetails model
export default interface EquipmentType {
  id: Number | null;
  title: string;
  num_available: Number;
  img_url: string;
  description: string;
  max_reservation_time: Number;
  items: EquipmentItem[];
}
