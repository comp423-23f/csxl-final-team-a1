import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import EquipmentType from '../../equipment/equipment-type.model';
import EquipmentItem from '../../equipment/equipment-item.model';

@Injectable({
  providedIn: 'root'
})
export class AdminEquipmentService {
  constructor(private http: HttpClient) {}

  getEquipmentType(id: Number): EquipmentType {
    let type: EquipmentType = {
      id: 1,
      description: 'default',
      img_url: 'none',
      max_reservation_time: -1,
      num_available: -1,
      title: 'placeholder',
      items: [
        { id: 1, display_status: false },
        { id: 2, display_status: true }
      ]
    };

    let types$ = this.getEquipmentTypes();
    types$.subscribe((types) => {
      for (let i = 0; i < types.length; i++) {
        if (types[i].id == id) {
          type = types[i];
        }
      }
    });

    return type;
  }

  getEquipmentTypes(): Observable<EquipmentType[]> {
    //TODO - replace this with a route returning type details, hopefully this fixes base page and edit
    return this.http.get<EquipmentType[]>('/api/equipment/list-all-equipments');
  }

  //TODO: POST new type to backend - change return type to Observable<EquipmentType[]>?
  createEquipmentType(new_type: EquipmentType): void {
    console.log(new_type);
  }

  //TODO: PUT type to backend - change return type to Observable<EquipmentType[]>?
  updateEquipmentType(updated_type: EquipmentType): void {
    console.log(updated_type);
  }

  //TODO: DELETE type from backend - change return type to Observable<EquipmentType[]>?
  deleteEquipmentType(type_id: Number): void {
    console.log(type_id);
  }

  //TODO: POST to server - change return type to Observable<EquipmentType[]>?
  createEquipmentItem(type_id: Number): void {
    console.log(type_id);
  }

  //TODO: DELETE on server
  deleteEquipmentItem(item_id: Number): void {
    console.log(item_id);
  }

  toggleDamaged(item_id: Number): void {
    console.log(item_id);
  }
}
