import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import EquipmentType from '../../equipment/equipment-type.model'

@Injectable({
  providedIn: 'root'
})
export class AdminEquipmentService {

  current_type: EquipmentType | null = null;

  constructor(private http: HttpClient) {
  }

  setCurrent(type: EquipmentType): void {
    this.current_type = type;
  }
  
  getCurrent(): EquipmentType | null {
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
  deleteEquipmentType(new_type: EquipmentType): void {
    console.log("TODO");
  }
}
