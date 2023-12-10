import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subscription } from 'rxjs';
import EquipmentReservation from '../equipment-reservation.model';
import { RxReservations } from './rx-reservations';
import { EquipmentReservationDetails } from '../equipment-reservation.model';

@Injectable({
  providedIn: 'root'
})
export class AmbassadorService {
  private reservations: RxReservations = new RxReservations();
  public reservations$: Observable<EquipmentReservationDetails[]> =
    this.reservations.value$;

  constructor(private http: HttpClient) {}

  getEquipmentReservations(): void {
    this.http
      .get<EquipmentReservationDetails[]>(
        '/api/equipment/ambassador-get-all-reservations'
      )
      .subscribe((reservations) => {
        this.reservations.set(reservations);
      });
  }

  activateReservation(reservation: EquipmentReservationDetails): void {
    this.http
      .put<EquipmentReservationDetails>(
        `/api/equipment/activate-reservation/${reservation.id}`,
        {}
      )
      .subscribe((reservation) => {
        this.reservations.updateReservation(reservation);
      });
  }

  returnReservation(
    reservation: EquipmentReservationDetails,
    return_description: string
  ): void {
    this.http
      .put<EquipmentReservationDetails>(
        `/api/equipment/check-in-equipment/${reservation.id}/${return_description}`,
        {}
      )
      .subscribe((reservation) => {
        this.reservations.updateReservation(reservation);
      });
  }

  cancelReservation(reservation: EquipmentReservationDetails) {
    this.http
      .delete<EquipmentReservationDetails>(
        `/api/equipment/ambassador-cancel-reservation/${reservation.id}`,
        {}
      )
      .subscribe({
        next: (_) => {
          this.reservations.remove(reservation);
        },
        error: (err) => {
          alert(err);
        }
      });
  }
}
