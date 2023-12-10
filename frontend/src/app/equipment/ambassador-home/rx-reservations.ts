import { RxObject } from 'src/app/rx-object';
import EquipmentReservation from '../equipment-reservation.model';
import ReservationDetails from '../reservation-details';

export class RxReservations extends RxObject<ReservationDetails[]> {
  updateReservation(updates: ReservationDetails) {
    let reservation = this.value.find((r) => r.id === updates.id);
    if (reservation) {
      Object.assign(reservation, updates);
    }
    this.notify();
  }

  remove(reservation: ReservationDetails) {
    this.value = this.value.filter((r) => r.id !== reservation.id);
    this.notify();
  }
}
