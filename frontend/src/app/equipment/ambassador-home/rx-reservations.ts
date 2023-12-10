import { RxObject } from 'src/app/rx-object';
import EquipmentReservation from '../equipment-reservation.model';
import { EquipmentReservationDetails } from '../equipment-reservation.model';

export class RxReservations extends RxObject<EquipmentReservationDetails[]> {
  updateReservation(updates: EquipmentReservationDetails) {
    let reservation = this.value.find((r) => r.id === updates.id);
    if (reservation) {
      Object.assign(reservation, updates);
    }
    this.notify();
  }

  remove(reservation: EquipmentReservationDetails) {
    this.value = this.value.filter((r) => r.id !== reservation.id);
    this.notify();
  }
}
