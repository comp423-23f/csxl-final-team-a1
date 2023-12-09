import { Component, Input } from '@angular/core';
import ReservationDetails from '../../reservation-details';
import EquipmentService from '../../equipment.service';
import { Router } from '@angular/router';

@Component({
  selector: 'equipment-reservation-card',
  templateUrl: './equipment-reservation-card.widget.html',
  styleUrls: ['./equipment-reservation-card.widget.css']
})
export class EquipmentReservationCard {
  /** Inputs and outputs go here */
  @Input() reservation!: ReservationDetails;

  /** Constructor */
  constructor(private equipment_service: EquipmentService) {}

  cancel() {
    this.equipment_service
      .cancelReservation(this.reservation.id)
      .subscribe((value: boolean) => {
        if (value) {
          location.reload();
        } else {
          console.log('ERROR: Reservation not cancelled.');
        }
      });
  }
}
