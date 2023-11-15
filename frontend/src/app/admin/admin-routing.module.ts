import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminComponent } from './admin.component';
import { AdminRoleDetailsComponent } from './roles/details/admin-role-details.component';
import { AdminRolesListComponent } from './roles/list/admin-roles-list.component';
import { AdminUsersListComponent } from './users/list/admin-users-list.component';
import { AdminOrganizationListComponent } from './organization/list/admin-organization-list.component';
import { AdminEquipmentBaseComponent } from './equipment/admin-equipment-base/admin-equipment-base.component';
import { AdminEquipmentCreateComponent } from './equipment/admin-equipment-create/admin-equipment-create.component';
import { AdminEquipmentEditComponent } from './equipment/admin-equipment-edit/admin-equipment-edit.component';

const routes: Routes = [
  {
    path: '',
    component: AdminComponent,
    children: [
      AdminUsersListComponent.Route,
      AdminRolesListComponent.Route,
      AdminRoleDetailsComponent.Route,
      AdminOrganizationListComponent.Route,
      AdminEquipmentBaseComponent.Route,
      AdminEquipmentCreateComponent.Route,
      AdminEquipmentEditComponent.Route
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule {}
