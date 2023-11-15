import { Component } from '@angular/core';
import EquipmentService from '../equipment.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-agreement',
  templateUrl: './agreement.component.html',
  styleUrls: ['./agreement.component.css']
})
export class AgreementComponent {
  constructor(
    private equipment: EquipmentService,
    private router: Router
  ) {}

  updateAgreementStatus() {
    this.equipment.updateAgreementStatus().subscribe((res) => {
      if (res === true) {
        this.router.navigate(['/equipment-reservations']);
      }
    });
  }
}
