import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import TypeDetails from '../../equipment/equipment-type.model';
import BaseEquipmentType from './base-equipment-type.model';
import EquipmentItem from '../../equipment/equipment-item.model';
import { AuthenticationService } from 'src/app/authentication.service';

@Injectable({
  providedIn: 'root'
})
export class AdminEquipmentService {
  constructor(
    private http: HttpClient,
    protected auth: AuthenticationService
  ) {}

  getEquipmentType(id: Number): Observable<TypeDetails> {
    return this.getEquipmentTypes().pipe(
      map((types: TypeDetails[]) => {
        let foundType: TypeDetails = {
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

  getEquipmentTypes(): Observable<TypeDetails[]> {
    return this.http.get<TypeDetails[]>('/api/equipment/get-all');
  }

  createEquipmentType(new_type: BaseEquipmentType): void {
    this.http
      .post<BaseEquipmentType>('/api/equipment/create-type', new_type)
      .subscribe();
  }

  updateEquipmentType(updated_type: BaseEquipmentType): void {
    this.http
      .put<BaseEquipmentType>('/api/equipment/modify-type', updated_type)
      .subscribe();
  }

  deleteEquipmentType(type_id: Number): void {
    this.http
      .delete<TypeDetails[]>(`/api/equipment/delete-type/${type_id}`)
      .subscribe();
  }

  createEquipmentItem(type_id: Number): void {
    this.http
      .post<TypeDetails[]>(`/api/equipment/create-item/${type_id}`, {})
      .subscribe();
  }

  deleteEquipmentItem(item_id: Number): void {
    this.http
      .delete<TypeDetails[]>(`/api/equipment/delete-item/${item_id}`)
      .subscribe();
  }

  toggleDamaged(item_id: Number, available: Boolean): void {
    this.http
      .put<EquipmentItem>(
        `/api/equipment/update-item?item_id=${item_id}&available=${available}`,
        {}
      )
      .subscribe();
  }
}
