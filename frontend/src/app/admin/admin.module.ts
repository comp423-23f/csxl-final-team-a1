import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { AdminComponent } from './admin.component';
import { AdminRoutingModule } from './admin-routing.module';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

import { AdminUsersListComponent } from './users/list/admin-users-list.component';
import { AdminRolesListComponent } from './roles/list/admin-roles-list.component';
import { AdminRoleDetailsComponent } from './roles/details/admin-role-details.component';
import { AdminOrganizationListComponent } from './organization/list/admin-organization-list.component';
import { AdminEquipmentBaseComponent } from './equipment/admin-equipment-base/admin-equipment-base.component';
import { AdminEquipmentEditComponent } from './equipment/admin-equipment-edit/admin-equipment-edit.component';
import { AdminEquipmentCreateComponent } from './equipment/admin-equipment-create/admin-equipment-create.component';

@NgModule({
  declarations: [
    AdminComponent,
    AdminUsersListComponent,
    AdminRolesListComponent,
    AdminRoleDetailsComponent,
    AdminOrganizationListComponent,
    AdminEquipmentBaseComponent,
    AdminEquipmentCreateComponent,
    AdminEquipmentEditComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    MatTabsModule,
    MatTableModule,
    MatDialogModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatListModule,
    MatAutocompleteModule,
    MatCardModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class AdminModule {}
