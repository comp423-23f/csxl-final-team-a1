import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatButton, MatButtonModule } from '@angular/material/button';

import { EquipmentRoutingModule } from './equipment-routing.module';
import { EquipmentDisplayComponent } from './equipment-display/equipment-display.component';
import { EquipmentCard } from './widgets/equipment_card/equipment-card.widget';
import { AgreementComponent } from './agreement/agreement.component';
import { CalendarSquare } from './widgets/calendar-square/calendar-square.widget';
import { ReserveScreenComponent } from './reserve-screen/reserve-screen.component';

@NgModule({
  declarations: [
    EquipmentDisplayComponent,
    EquipmentCard,
    AgreementComponent,
    CalendarSquare,
    ReserveScreenComponent
  ],
  imports: [
    EquipmentRoutingModule,
    CommonModule,
    MatCardModule,
    MatButtonModule
  ]
})
export class EquipmentModule {}
