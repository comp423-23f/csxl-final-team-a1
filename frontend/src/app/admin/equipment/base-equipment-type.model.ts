//This model aligns with the backend's Pydantic EquipmentType model

export default interface BaseEquipmentType {
  id: Number | null;
  title: string;
  num_available: Number;
  img_url: string;
  description: string;
  max_reservation_time: Number;
}
