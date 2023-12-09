import { Component, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import TypeDetails from '../equipment-type.model';
import EquipmentService from '../equipment.service';
import { AuthenticationService } from 'src/app/authentication.service';
import { Router } from '@angular/router';
import ReservationDetails from '../reservation-details';

@Component({
  selector: 'app-equipment-display',
  templateUrl: './equipment-display.component.html',
  styleUrls: ['./equipment-display.component.css']
})
export class EquipmentDisplayComponent implements OnInit {
  public static route = {
    path: '',
    component: EquipmentDisplayComponent,
    children: []
  };
  private static DATES_PAST_TO_SHOW: number = 6;

  constructor(
    private equipment: EquipmentService,
    private router: Router
  ) {}

  ngOnInit() {
    this.equipment.getAgreementStatus().subscribe((res) => {
      if (res === false) {
        this.router.navigate(['/equipment-reservations/agreement']);
      }
    });
  }

  types$: Observable<TypeDetails[]> = this.equipment.getEquipmentTypes();
  reservations$: Observable<ReservationDetails[]> =
    this.equipment.getUserReservations();

  notTooFar(reservation: ReservationDetails): boolean {
    let date: Date | null = reservation.actual_return_date;
    return (
      date === null ||
      Date.now() - date.getTime() >
        EquipmentDisplayComponent.DATES_PAST_TO_SHOW * 8.64 * 10 ** 7
    );
  }
}
