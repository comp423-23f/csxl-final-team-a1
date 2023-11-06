import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import EquipmentType from './equipment-type.model';

@Injectable({
  providedIn: 'root'
})
export default class EquipmentService {

  constructor(private http: HttpClient) { }

  //Return equipment types - dummy data, soon to be replaced by GET request data
  getEquipmentTypes(): Observable<EquipmentType[]> {
    return this.http.get<EquipmentType[]>("/api/equipment/list-all-equipments");
  }
}

/* {id: 2,
            title: "iPad",
            num_available: 3,
            img_url: "https://s.yimg.com/uu/api/res/1.2/vVXUm8VfTF7kLKvCIqrKjg--~B/Zmk9ZmlsbDtoPTEyNzA7dz0yNDcwO2FwcGlkPXl0YWNoeW9u/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2021-05/6c1a9ec0-b815-11eb-8b33-87fbb637229f.cf.jpg",
            description: "Tablet device",
            max_reservation_time: 3} */
