import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, tap } from 'rxjs';
import TypeDetails from '../../equipment/equipment-type.model';
import BaseEquipmentType from './base-equipment-type.model';
import EquipmentItem from '../../equipment/equipment-item.model';
import { AuthenticationService } from 'src/app/authentication.service';
import { RxItem } from '../../equipment/rx-item';

@Injectable({
  providedIn: 'root'
})
export class AdminEquipmentService {
  constructor(
    private http: HttpClient,
    protected auth: AuthenticationService
  ) {}

  private items: RxItem = new RxItem();
  public items$: Observable<EquipmentItem[]> = this.items.value$;

  listItems(type_id: Number): void {
    this.getEquipmentTypes().subscribe((types) => {
      for (let i = 0; i < types.length; i++) {
        if (types[i].id == type_id) {
          this.items.set(types[i].items);
        }
      }
    });
  }

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
      .delete<TypeDetails>(`/api/equipment/delete-type/${type_id}`)
      .subscribe();
  }

  createEquipmentItem(type_id: Number): Observable<void> {
    return this.http
      .post<EquipmentItem>(`/api/equipment/create-item/${type_id}`, {})
      .pipe(
        map((item) => {
          this.items.pushItem(item);
          this.listItems(type_id);
        })
      );
  }

  deleteEquipmentItem(item_id: Number): Observable<void> {
    return this.http
      .delete<EquipmentItem>(`/api/equipment/delete-item/${item_id}`)
      .pipe(
        map((item) => {
          this.items.removeItem(item);
        })
      );
  }

  toggleDamaged(item_id: Number, available: Boolean): Observable<void> {
    return this.http
      .put<EquipmentItem>(
        `/api/equipment/update-item?item_id=${item_id}&available=${available}`,
        {}
      )
      .pipe(
        map((item) => {
          this.items.updateItem(item);
        })
      );
  }
}
