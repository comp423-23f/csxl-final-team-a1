import { Component } from '@angular/core';
import EquipmentType from '../../../equipment/equipment-type.model';
import EquipmentItem from '../../../equipment/equipment-item.model';
import { AdminEquipmentService } from '../admin-equipment.service';
import { permissionGuard } from 'src/app/permission.guard';
import { Observable, map } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { equipmentTypeResolver } from '../equipment-type.resolver';
import BaseEquipmentType from '../base-equipment-type.model';

@Component({
  selector: 'app-admin-equipment-edit',
  templateUrl: './admin-equipment-edit.component.html',
  styleUrls: ['./admin-equipment-edit.component.css']
})
export class AdminEquipmentEditComponent {
  public static Route = {
    path: 'equipment/edit/:id',
    component: AdminEquipmentEditComponent,
    title: 'Equipment Administration',
    canActivate: [permissionGuard('equipment', 'equipment/')],
    resolve: {
      type: equipmentTypeResolver
    }
  };

  public adminPermission$: Observable<boolean>;
  public items$: Observable<EquipmentItem[]>;

  /** Add validators to the form */
  title = new FormControl('', [Validators.required]);
  img_url = new FormControl('', [Validators.required]);
  description = new FormControl('', [
    Validators.required,
    Validators.maxLength(150)
  ]);
  max_reservation_time = new FormControl('', [
    Validators.required,
    Validators.min(1),
    Validators.pattern('^[0-9]*$')
  ]);

  /** Equipment Type edit Form */
  public equipmentTypeForm = this.formBuilder.group({
    title: this.title,
    img_url: this.img_url,
    description: this.description,
    max_reservation_time: this.max_reservation_time
  });

  public displayedColumns: string[] = [
    'id',
    'display_status',
    'damaged',
    'actions'
  ];

  public current: EquipmentType;

  constructor(
    private route: ActivatedRoute,
    protected formBuilder: FormBuilder,
    private adminEquipment: AdminEquipmentService,
    private permission: PermissionService,
    private router: Router
  ) {
    this.adminPermission$ = this.permission.check('admin.view', 'admin/');

    const data = this.route.snapshot.data as {
      type: EquipmentType;
    };
    this.current = data.type;

    this.items$ = adminEquipment.items$.pipe(
      map((items) =>
        items.slice().sort((a, b) => {
          return a.id!.valueOf() - b.id!.valueOf();
        })
      )
    );
    if (this.current.id == null) {
      this.router.navigate(['admin', 'equipment']);
    } else {
      adminEquipment.listItems(this.current.id);
    }

    this.equipmentTypeForm.setValue({
      title: this.current.title,
      img_url: this.current.img_url,
      description: this.current.description,
      max_reservation_time: String(this.current.max_reservation_time)
    });
  }

  onSave(): void {
    if (this.equipmentTypeForm.valid) {
      let type: BaseEquipmentType = {
        id: this.current.id,
        title: String(this.equipmentTypeForm.value.title),
        description: String(this.equipmentTypeForm.value.description),
        img_url: String(this.equipmentTypeForm.value.img_url),
        max_reservation_time: Number(
          this.equipmentTypeForm.value.max_reservation_time
        ),
        num_available: Number(this.current.num_available)
      };

      this.adminEquipment.updateEquipmentType(type);
      this.router.navigate(['admin', 'equipment']);
    }
  }

  onDelete(): void {
    if (this.current.id) {
      this.adminEquipment.deleteEquipmentType(this.current.id);
    }
    this.router.navigate(['admin', 'equipment']);
  }

  deleteEquipmentItem(item_id: Number): void {
    this.adminEquipment.deleteEquipmentItem(item_id).subscribe();
    this.router.navigate([
      'admin',
      'equipment',
      'edit',
      String(this.current.id)
    ]);
  }

  createEquipmentItem(type_id: Number): void {
    this.adminEquipment.createEquipmentItem(type_id).subscribe();
    this.router.navigate([
      'admin',
      'equipment',
      'edit',
      String(this.current.id)
    ]);
  }

  toggleDamaged(item_id: Number, available: Boolean): void {
    this.adminEquipment.toggleDamaged(item_id, available).subscribe();
    this.router.navigate([
      'admin',
      'equipment',
      'edit',
      String(this.current.id)
    ]);
  }
}
