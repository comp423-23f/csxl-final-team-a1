import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatButton, MatButtonModule } from '@angular/material/button';

import { EquipmentRoutingModule } from './equipment-routing.module';
import { EquipmentDisplayComponent } from './equipment-display/equipment-display.component';
import { EquipmentCard } from './widgets/equipment_card/equipment-card.widget';
import { AgreementComponent } from './agreement/agreement.component';

@NgModule({
  declarations: [EquipmentDisplayComponent, EquipmentCard, AgreementComponent],
  imports: [
    EquipmentRoutingModule,
    CommonModule,
    MatCardModule,
    MatButtonModule
  ]
})
export class EquipmentModule {}
