import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EquipmentDisplayComponent } from './equipment-display/equipment-display.component';
import { AgreementComponent } from './agreement/agreement.component';
import { AmbassadorHomeComponent } from './ambassador-home/ambassador-home.component';
import { ReserveScreenComponent } from './reserve-screen/reserve-screen.component';

const routes: Routes = [
  AmbassadorHomeComponent.Route,
  EquipmentDisplayComponent.route,
  AgreementComponent.route,
  ReserveScreenComponent.route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EquipmentRoutingModule {}
