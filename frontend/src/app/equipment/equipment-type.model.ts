import EquipmentItem from './equipment-item.model';

//This model aligns with the backends Pydantic TypeDetails model
export default interface TypeDetails {
  id: number | null;
  title: string;
  num_available: number;
  img_url: string;
  description: string;
  max_reservation_time: number;
  items: EquipmentItem[];
}
