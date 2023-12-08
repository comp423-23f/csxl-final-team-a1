export default interface EquipmentReservation {
  id: number | null;
  item_id: number;
  type_id: number;
  user_id: number;
  check_out_date: string;
  ambassador_check_out: boolean;
  expected_return_date: string;
  actual_return_date: string | null;
  return_description: string | null;
}
