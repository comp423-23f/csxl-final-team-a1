import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EquipmentDisplayComponent } from './equipment-display/equipment-display.component';

const routes: Routes = [
    {
        path: '',
        component: EquipmentDisplayComponent,
        children: []
      }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EquipmentRoutingModule {}