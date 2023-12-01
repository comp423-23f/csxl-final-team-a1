export default interface EquipmentReservation {
  id: Number | null;
  item_id: Number;
  user_id: Number;
  check_out_date: Date;
  ambassador_check_out: boolean;
  expected_return_date: Date;
  actual_return_date: Date;
  return_description: string;
}
