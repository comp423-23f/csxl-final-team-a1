import { Injectable } from '@angular/core';
import { HttpClient, HttpContext } from '@angular/common/http';
import { Observable, Subscription } from 'rxjs';
import TypeDetails from './equipment-type.model';
import { Profile } from '../models.module';
import { AuthenticationService } from '../authentication.service';
import { ProfileService } from '../profile/profile.service';
import ItemDetails from './item-details.model';
import EquipmentReservation from './equipment-reservation.model';
import ReservationDetails from './reservation-details';

@Injectable({
  providedIn: 'root'
})
export default class EquipmentService {
  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  constructor(
    private http: HttpClient,
    private auth: AuthenticationService,
    private profileService: ProfileService
  ) {
    this.profileSubscription = this.profileService.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  //Return equipment types requested from backend.
  getEquipmentTypes(): Observable<TypeDetails[]> {
    return this.http.get<TypeDetails[]>('/api/equipment/list-all-equipments');
  }

  getAgreementStatus(): Observable<boolean> {
    let pid: number = 0;
    if (this.profile !== undefined) {
      pid = this.profile.pid;
    }
    return this.http.get<boolean>(
      '/api/equipment/get-user-agreement-status/' + pid
    );
  }

  updateAgreementStatus(): Observable<boolean> {
    let pid: number = 0;
    let onyen: string = '';
    if (this.profile !== undefined) {
      pid = this.profile.pid;
      onyen = this.profile.onyen;
    }

    return this.http.put<boolean>(
      '/api/equipment/update-user-agreement-status',
      [pid, onyen]
    );
  }

  getTypeAvailability(type_id: number): Observable<ItemDetails[]> {
    return this.http.get<ItemDetails[]>(
      '/api/equipment/get-item-details-from-type/' + type_id
    );
  }

  createReservation(
    reservation: EquipmentReservation
  ): Observable<ReservationDetails> {
    return this.http.post<ReservationDetails>(
      '/api/equipment/create-reservation',
      reservation
    );
  }

  cancelReservation(reservation_id: number): Observable<boolean> {
    return this.http.delete<boolean>(
      '/api/equipment/cancel-reservation/' + reservation_id
    );
  }

  getUserReservations(): Observable<ReservationDetails[]> {
    return this.http.get<ReservationDetails[]>(
      '/api/equipment/get-user-equipment-reservations'
    );
  }
}
