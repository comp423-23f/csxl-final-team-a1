import { Component } from '@angular/core';
import EquipmentType from '../../../equipment/equipment-type.model';
import { UpdatedEquipmentType } from '../updated-equipment-type.model';
import EquipmentItem from '../../../equipment/equipment-item.model';
import { AdminEquipmentService } from '../admin-equipment.service';
import { permissionGuard } from 'src/app/permission.guard';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-equipment-edit',
  templateUrl: './admin-equipment-edit.component.html',
  styleUrls: ['./admin-equipment-edit.component.css']
})
export class AdminEquipmentEditComponent {
  public static Route = {
    path: 'equipment/edit',
    component: AdminEquipmentEditComponent,
    title: 'Equipment Administration',
    canActivate: [permissionGuard('equipment', 'equipment/')]
  };

  public adminPermission$: Observable<boolean>;

  /** Add validators to the form */
  title = new FormControl('', [Validators.required]);
  img_url = new FormControl('', [Validators.required]);
  description = new FormControl('', [
    Validators.required,
    Validators.maxLength(150),
  ]);
  max_reservation_time = new FormControl('', [Validators.required,Validators.min(1), Validators.pattern("^[0-9]*$"),]);

  /** Equipment Type edit Form */
  public equipmentTypeForm = this.formBuilder.group({
    title: this.title,
    img_url: this.img_url,
    description: this.description,
    max_reservation_time: this.max_reservation_time
  });

  public displayedColumns: string[] = ['id', 'display_status', 'actions'];

  //replace type with Observable<EquipmentType[]>
  items$: EquipmentItem[]; 
  current: EquipmentType;

  constructor(protected formBuilder: FormBuilder, private adminEquipment: AdminEquipmentService, private permission: PermissionService, private router: Router) {
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');

    this.current = this.adminEquipment.getCurrent();
    if (this.current.id == -1) {
      this.router.navigate(['admin', 'equipment']);
    }

    // Set equipment edit form data
    this.equipmentTypeForm.setValue({
      title: this.current.title,
      img_url: this.current.img_url,
      description: this.current.description,
      max_reservation_time: String(this.current.max_reservation_time)
    });
    this.items$ = this.adminEquipment.getItems(this.current.id);
    console.log(this.items$);
  }

  onSave(): void {
    if (this.equipmentTypeForm.valid) {
      let type = {'title':'', 'description':'', 'img_url':'', 'max_reservation_time':-1};
      Object.assign(type, this.equipmentTypeForm.value);

      this.adminEquipment.updateEquipmentType(type);
      this.router.navigate(['admin', 'equipment']);
    }
  }

  onDelete(): void {
    this.adminEquipment.deleteEquipmentType(this.current.id);
    this.router.navigate(['admin', 'equipment','edit']);  
  }

  deleteEquipmentItem(item_id: Number): void {
    this.adminEquipment.deleteEquipmentItem(item_id);
    this.router.navigate(['admin', 'equipment','edit']);  
  }

  createEquipmentItem(type_id: Number): void {
    this.adminEquipment.deleteEquipmentType(type_id);
    this.router.navigate(['admin', 'equipment','edit']);  
  }

}
