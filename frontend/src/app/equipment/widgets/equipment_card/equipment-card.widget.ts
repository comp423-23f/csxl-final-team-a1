import { Component, Input, EventEmitter, Output } from '@angular/core';
import TypeDetails from '../../equipment-type.model';
import { Router } from '@angular/router';

@Component({
  selector: 'equipment-card',
  templateUrl: './equipment-card.widget.html',
  styleUrls: ['./equipment-card.widget.css']
})
export class EquipmentCard {
  /** Inputs and outputs go here */
  @Input() type!: TypeDetails;

  @Output() output = new EventEmitter<TypeDetails>();

  /** Constructor */
  constructor(private router: Router) {}

  onClick() {
    this.router.navigate([
      '/equipment-reservations',
      'reserve-screen',
      this.type.id
    ]);
  }
}
