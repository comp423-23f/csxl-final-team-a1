import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import EquipmentType from '../../equipment/equipment-type.model';
import { NewEquipmentType } from './new-equipment-type.model';
import EquipmentItem from '../../equipment/equipment-item.model';

@Injectable({
  providedIn: 'root'
})
export class AdminEquipmentService {

  current_type: EquipmentType = {'id':-1, 'description':'default', 'img_url':'none', 'max_reservation_time': -1, 'num_available': -1, 'title':'placeholder'};

  constructor(private http: HttpClient) {
  }

  setCurrent(type: EquipmentType): void {
    this.current_type = type;
  }
  
  getCurrent(): EquipmentType {
    return this.current_type;
  }

  //need to update this with a new route that returns total number of equipment for num_avail
  getEquipmentTypes(): Observable<EquipmentType[]> {
    return this.http.get<EquipmentType[]>("/api/equipment/list-all-equipments");
  }

  //TODO: POST new type to backend
  createEquipmentType(new_type: NewEquipmentType): void {
    console.log(new_type);
  }

  //TODO: PUT type to backend
  updateEquipmentType(updated_type: EquipmentType): void {
    console.log(updated_type);
  }

  //TODO: DELETE type from backend
  deleteEquipmentType(type_id: Number): void {
    console.log(type_id);
  }

  //TODO: POST to server
  createEquipmentItem(type_id: Number): void {
    console.log(type_id);
  }

  //TODO: DELETE on server
  deleteEquipmentItem(item_id: Number): void {
    console.log(item_id);
  }

  //TODO: Unsure about method but request all items for a type from the backend - this might end up being a type details object, if it is need to change the EquipmentItem interface
  getItems(type_id: Number): EquipmentItem[] {
    return [{'id':1, 'display_status':false},{'id':2, 'display_status':true}]
  }
}
