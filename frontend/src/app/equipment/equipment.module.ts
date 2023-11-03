import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EquipmentDisplayComponent } from './equipment-display/equipment-display.component';
import { EquipmentCard } from './widgets/equipment_card/equipment-card.widget';
import { MatCardModule } from '@angular/material/card';
import { EquipmentRoutingModule } from './equipment-routing.module';



@NgModule({
  declarations: [
    EquipmentDisplayComponent,
    EquipmentCard
  ],
  imports: [
    EquipmentRoutingModule,
    CommonModule,
    MatCardModule,
  ]
})
export class EquipmentModule { }
