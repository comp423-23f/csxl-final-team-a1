//This model aligns with the backend's Pydantic EquipmentType model

export default interface BaseEquipmentType {
  id: Number | null;
  title: String;
  img_url: String;
  num_available: Number;
  description: String;
  max_reservation_time: Number;
}
