import { Component } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { Observable } from 'rxjs';
import { NewEquipmentType } from '../new-equipment-type.model';
import EquipmentType from '../../../equipment/equipment-type.model';
import { AdminEquipmentService } from '../admin-equipment.service';
import { permissionGuard } from 'src/app/permission.guard';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
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
  count = new FormControl('', [Validators.required, Validators.min(1), Validators.pattern("^[0-9]*$"),]);
  description = new FormControl('', [
    Validators.required,
    Validators.maxLength(150),
  ]);
  max_reservation_time = new FormControl('', [Validators.required,Validators.min(1), Validators.pattern("^[0-9]*$"),]);

  /** Equipment Type Creation Form */
  public equipmentTypeForm = this.formBuilder.group({
    title: this.title,
    count: this.count,
    img_url: this.img_url,
    description: this.description,
    max_reservation_time: this.max_reservation_time
  });

  constructor(protected formBuilder: FormBuilder, private adminEquipment: AdminEquipmentService, private permission: PermissionService, private router: Router) {
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
  }

  onSubmit(): void {
    if (this.equipmentTypeForm.valid) {
      let new_type = {'title':'', 'description':'', 'count':-1, 'img_url':'', 'max_reservation_time':-1};
      Object.assign(new_type, this.equipmentTypeForm.value);
      
      this.adminEquipment.createEquipmentType(new_type);
      this.router.navigate(['admin', 'equipment']);
    }
  }
}
