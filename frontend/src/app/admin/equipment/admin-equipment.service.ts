import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import EquipmentType from '../../equipment/equipment-type.model';
import EquipmentItem from '../../equipment/equipment-item.model';

@Injectable({
  providedIn: 'root'
})
export class AdminEquipmentService {

  current_type: EquipmentType = {'id':-1, 'description':'default', 'img_url':'none', 'max_reservation_time': 3, 'num_available': 3, 'title':'placeholder'};

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
  createEquipmentType(new_type: EquipmentType): void {
    console.log("TODO");
  }

  //TODO: PUT type to backend
  updateEquipmentType(updated_type: EquipmentType): void {
    console.log("TODO");
  }

  //TODO: DELETE type from backend
  deleteEquipmentType(type_id: EquipmentType): void {
    console.log("TODO");
  }

  //TODO: Unsure about method but request all items for a type from the backend
  getItems(type_id: Number): EquipmentItem[] {
    return [{'id':1, 'display_status':false},{'id':2, 'display_status':true}]
  }
}
