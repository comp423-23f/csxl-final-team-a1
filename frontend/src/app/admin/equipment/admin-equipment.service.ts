import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import EquipmentType from '../../equipment/equipment-type.model';
import EquipmentItem from '../../equipment/equipment-item.model';

@Injectable({
  providedIn: 'root'
})
export class AdminEquipmentService {
  constructor(private http: HttpClient) {}

  getEquipmentType(id: number): Observable<EquipmentType> {
    return this.getEquipmentTypes().pipe(
      map((types: EquipmentType[]) => {
        let foundType: EquipmentType = {
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

        for (let i = 0; i < types.length; i++) {
          if (types[i].id === id) {
            foundType = types[i];
            break;
          }
        }

        return foundType;
      })
    );
  }

  getEquipmentTypes(): Observable<EquipmentType[]> {
    return this.http.get<EquipmentType[]>('/api/equipment/get-all');
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
