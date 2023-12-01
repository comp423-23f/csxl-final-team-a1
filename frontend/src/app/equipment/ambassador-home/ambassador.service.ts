import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subscription } from 'rxjs';
import EquipmentReservation from '../equipment-reservation.model';


@Injectable({
  providedIn: 'root'
})
export class AmbassadorService {
  constructor(private http: HttpClient) {}

  getEquipmentReservations(): Observable<EquipmentReservation[]> {
    // API route here
  }

  activateReservation(): Observable<EquipmentReservation> {
    // API route here
  }

  returnReservation(): Observable<EquipmentReservation> {
    // API route here
  }
}
