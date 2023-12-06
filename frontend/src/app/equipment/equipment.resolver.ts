import ItemDetails from './item-details.model';
import EquipmentService from './equipment.service';
import { ResolveFn } from '@angular/router';
import { inject } from '@angular/core';

export const calendarResolver: ResolveFn<ItemDetails[]> = (route, state) => {
  let type_id = Number(route.paramMap.get('type_id'));
  return inject(EquipmentService).getTypeAvailability(type_id);
};
