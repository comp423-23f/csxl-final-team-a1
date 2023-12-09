import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';

import { EquipmentRoutingModule } from './equipment-routing.module';
import { EquipmentDisplayComponent } from './equipment-display/equipment-display.component';
import { EquipmentCard } from './widgets/equipment_card/equipment-card.widget';
import { AgreementComponent } from './agreement/agreement.component';
import { AmbassadorHomeComponent } from './ambassador-home/ambassador-home.component';
import { DescriptionComponent } from './ambassador-home/ambassador-home.component';

@NgModule({
  declarations: [
    EquipmentDisplayComponent,
    EquipmentCard,
    AgreementComponent,
    AmbassadorHomeComponent,
    DescriptionComponent
  ],
  imports: [
    EquipmentRoutingModule,
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule
  ]
})
export class EquipmentModule {}
