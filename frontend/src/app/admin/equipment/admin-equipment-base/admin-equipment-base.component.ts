import { Component } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { Observable } from 'rxjs';
import EquipmentType from '../../../equipment/equipment-type.model';
import { AdminEquipmentService } from '../admin-equipment.service';
import { permissionGuard } from 'src/app/permission.guard';

@Component({
  selector: 'app-admin-equipment-base',
  templateUrl: './admin-equipment-base.component.html',
  styleUrls: ['./admin-equipment-base.component.css']
})
export class AdminEquipmentBaseComponent {
  public static Route = {
    path: 'equipment',
    component: AdminEquipmentBaseComponent,
    title: 'Equipment Administration',
    canActivate: [permissionGuard('equipment', 'equipment/')]
  };

  constructor(private equipment: AdminEquipmentService) {}

  public displayedColumns: string[] = ['name', 'count'];
  types$: Observable<EquipmentType[]> = this.equipment.getEquipmentTypes();

}
