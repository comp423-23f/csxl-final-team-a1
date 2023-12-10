import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subscription } from 'rxjs';
import EquipmentReservation from '../equipment-reservation.model';
import { RxReservations } from './rx-reservations';
import ReservationDetails from '../reservation-details';

@Injectable({
  providedIn: 'root'
})
export class AmbassadorService {
  private reservations: RxReservations = new RxReservations();
  public reservations$: Observable<ReservationDetails[]> =
    this.reservations.value$;

  constructor(private http: HttpClient) {}

  getEquipmentReservations(): void {
    this.http
      .get<ReservationDetails[]>(
        '/api/equipment/ambassador-get-all-reservations'
      )
      .subscribe((reservations) => {
        this.reservations.set(reservations);
      });
  }

  activateReservation(reservation: ReservationDetails): void {
    this.http
      .put<ReservationDetails>(
        `/api/equipment/activate-reservation/${reservation.id}`,
        {}
      )
      .subscribe((reservation) => {
        this.reservations.updateReservation(reservation);
      });
  }

  returnReservation(
    reservation: ReservationDetails,
    return_description: string
  ): void {
    this.http
      .put<ReservationDetails>(
        `/api/equipment/check-in-equipment/${reservation.id}/${return_description}`,
        {}
      )
      .subscribe((reservation) => {
        this.reservations.updateReservation(reservation);
      });
  }

  cancelReservation(reservation: ReservationDetails) {
    this.http
      .delete<ReservationDetails>(
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
