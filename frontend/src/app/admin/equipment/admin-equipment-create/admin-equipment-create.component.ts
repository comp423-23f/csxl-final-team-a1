import { Component } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { Observable } from 'rxjs';
import EquipmentType from '../../../equipment/equipment-type.model';
import { AdminEquipmentService } from '../admin-equipment.service';
import { permissionGuard } from 'src/app/permission.guard';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatCardActions } from '@angular/material/card';
import { PermissionService } from 'src/app/permission.service';

@Component({
  selector: 'app-admin-equipment-create',
  templateUrl: './admin-equipment-create.component.html',
  styleUrls: ['./admin-equipment-create.component.css']
})
export class AdminEquipmentCreateComponent {
  public static Route = {
    path: 'equipment/new',
    component: AdminEquipmentCreateComponent,
    title: 'Equipment Administration',
    canActivate: [permissionGuard('equipment', 'equipment/')]
  };

  public adminPermission$: Observable<boolean>;

  /** Add validators to the form */
  title = new FormControl('', [Validators.required]);
  img_url = new FormControl('', [Validators.required]);
  count = new FormControl('', [Validators.required, Validators.min(1)]);
  description = new FormControl('', [
    Validators.required,
    Validators.maxLength(150)
  ]);
  max_reservation_time = new FormControl('', [Validators.min(1)]);

  /** Equipment Type Creation Form */
  public equipmentTypeForm = this.formBuilder.group({
    title: this.title,
    count: this.count,
    img_url: this.img_url,
    description: this.description,
    max_reservation_time: this.max_reservation_time
  });

  constructor(protected formBuilder: FormBuilder, private adminEquipment: AdminEquipmentService, private permission: PermissionService) {
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
  }

  onSubmit(): void {
    if (this.equipmentTypeForm.valid) {
      const newType: EquipmentType = { title: (this.registerForm.value.name as string), num_available: (this.registerForm.value.count as Number), img_url: (this.registerForm.value.img_url as string), description: (this.registerForm.value.description as string), max_reservation_time: (this.registerForm.value.max_reservation_time as Number)  }
    }



  }

}
