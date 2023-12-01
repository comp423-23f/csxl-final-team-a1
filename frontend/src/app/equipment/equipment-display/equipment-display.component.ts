import { Component, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import EquipmentType from '../equipment-type.model';
import EquipmentService from '../equipment.service';
import { AuthenticationService } from 'src/app/authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-equipment-display',
  templateUrl: './equipment-display.component.html',
  styleUrls: ['./equipment-display.component.css']
})
export class EquipmentDisplayComponent implements OnInit {
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

  types$: Observable<EquipmentType[]> = this.equipment.getEquipmentTypes();
}
