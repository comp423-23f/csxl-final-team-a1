export default interface EquipmentReservation {
  item_id: number;
  user_id: number;
  check_out_date: Date;
  ambassador_check_out: boolean;
  expected_return_date: Date;
  actual_return_date: Date | null;
  return_description: string;
}
