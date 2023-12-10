import { Profile } from '../models.module';
import EquipmentItem from './equipment-item.model';
import EquipmentType from './equipment-type.model';

export default interface EquipmentReservation {
  id: number;
  item_id: number;
  type_id: number;
  user_id: number;
  check_out_date: Date;
  ambassador_check_out: boolean;
  expected_return_date: Date;
  actual_return_date: Date | null;
  return_description: string | null;
  additional_description: string | null;
}

export interface EquipmentReservationDetails extends EquipmentReservation {
  item: EquipmentItem;
  user: Profile;
  type: EquipmentType;
}
