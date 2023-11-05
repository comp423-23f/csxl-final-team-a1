import { Component, Input } from '@angular/core';
import EquipmentType from '../../equipment-type.model';

@Component({
    selector: 'equipment-card',
    templateUrl: './equipment-card.widget.html',
    styleUrls: ['./equipment-card.widget.css']
})
export class EquipmentCard {
  /** Inputs and outputs go here */
  @Input() type!: EquipmentType;

  /** Constructor */
  constructor() { }
}