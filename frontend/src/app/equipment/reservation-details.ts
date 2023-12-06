import { Profile } from '../profile/profile.service';
import EquipmentItem from './equipment-item.model';
import EquipmentType from './type.model';

export default interface ReservationDetails {
  item_id: number | null;
  user_id: number;
  check_out_date: Date;
  ambassador_check_out: boolean;
  expected_return_date: Date;
  actual_return_date: Date | null;
  return_description: string;
  item: EquipmentItem;
  type: EquipmentType;
  user: Profile;
}
