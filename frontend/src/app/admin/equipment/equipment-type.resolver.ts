import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import EquipmentType from '../../equipment/equipment-type.model';
import { AdminEquipmentService } from './admin-equipment.service';

export const equipmentTypeResolver: ResolveFn<EquipmentType | undefined> = (
    route,
    state
  ) => {
      return inject(AdminEquipmentService).getEquipmentType(
        Number(route.paramMap.get('id')!)
      );
}

