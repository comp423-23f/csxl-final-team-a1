import { Component } from '@angular/core';
import EquipmentType from '../../../equipment/equipment-type.model';
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
  count = new FormControl('', [Validators.required, Validators.min(1), Validators.pattern("^[0-9]*$"),]);
  description = new FormControl('', [
    Validators.required,
    Validators.maxLength(150),
  ]);
  max_reservation_time = new FormControl('', [Validators.required,Validators.min(1), Validators.pattern("^[0-9]*$"),]);

  /** Equipment Type edit Form */
  public equipmentTypeForm = this.formBuilder.group({
    title: this.title,
    count: this.count,
    img_url: this.img_url,
    description: this.description,
    max_reservation_time: this.max_reservation_time
  });

  //Dummy data, we probably need a resolver here like was used in the organization editor
  public edited: EquipmentType = {id:5, title:"iPad", num_available:3, img_url:"google.com", description:"Hello", max_reservation_time:3}

  constructor(protected formBuilder: FormBuilder, private adminEquipment: AdminEquipmentService, private permission: PermissionService) {
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');
    /** Set equipment edit form data */
    this.equipmentTypeForm.setValue({
      title: this.edited.title,
      count: String(this.edited.num_available),
      img_url: this.edited.img_url,
      description: this.edited.description,
      max_reservation_time: String(this.edited.max_reservation_time),
    });
  }


  onSave(): void {
    //TODO - PUT edited type to the server and handle returned object
    console.log("saved");
  }

  onDelete(): void {
    //TODO - DELETE type from server
    console.log("deleted");
  }

}
