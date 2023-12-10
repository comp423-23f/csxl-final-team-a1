import { inject } from '@angular/core';
import { ResolveFn } from '@angular/router';
import TypeDetails from '../../equipment/equipment-type.model';
import { AdminEquipmentService } from './admin-equipment.service';

export const equipmentTypeResolver: ResolveFn<TypeDetails | undefined> = (
  route,
  state
) => {
  return inject(AdminEquipmentService).getEquipmentType(
    Number(route.paramMap.get('id')!)
  );
};
