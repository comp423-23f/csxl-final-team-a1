import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import EquipmentType from '../equipment-type.model';
import EquipmentService from '../equipment.service';

@Component({
  selector: 'app-equipment-display',
  templateUrl: './equipment-display.component.html',
  styleUrls: ['./equipment-display.component.css']
})
export class EquipmentDisplayComponent {
  constructor(private equipment: EquipmentService) {}

  types$: Observable<EquipmentType[]> = this.equipment.getEquipmentTypes();
}
