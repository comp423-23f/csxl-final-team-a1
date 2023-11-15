import { Component } from '@angular/core';
import EquipmentType from '../../../equipment/equipment-type.model';
import EquipmentItem from '../../../equipment/equipment-item.model';
import { AdminEquipmentService } from '../admin-equipment.service';
import { permissionGuard } from 'src/app/permission.guard';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { FormBuilder, FormControl, Validators } from '@angular/forms';

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

  constructor(protected formBuilder: FormBuilder, private adminEquipment: AdminEquipmentService, private permission: PermissionService) {
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');

    const current = this.adminEquipment.getCurrent();
    // Set equipment edit form data
    this.equipmentTypeForm.setValue({
      title: current.title,
      img_url: current.img_url,
      description: current.description,
      max_reservation_time: String(current.max_reservation_time)
    });
    this.items$ = this.adminEquipment.getItems(current.id);
    console.log(this.items$);
  }


  onSave(): void {
    //TODO - PUT edited type to the server and handle returned object
    console.log("saved");
  }

  onDelete(): void {
    //TODO - DELETE type from server
    console.log("deleted");
  }

  deleteEquipmentItem(): void {
    //TODO - DELETE equipment item from server
    console.log("deleted");
  }

  addEquipmentItem(): void {
    //TODO - POST equipment item to server, generate id automatically
    console.log("deleted");
  }

}
