import { Injectable } from '@angular/core';
import EquipmentType from './equipment-type.model';

@Injectable({
  providedIn: 'root'
})
export default class EquipmentService {

  constructor() { }

  //Return equipment types - dummy data, soon to be replaced by GET request data
  getEquipmentTypes(): EquipmentType[] {
    return [{id: 2,
            title: "iPad", 
              img_url: "https://s.yimg.com/uu/api/res/1.2/vVXUm8VfTF7kLKvCIqrKjg--~B/Zmk9ZmlsbDtoPTEyNzA7dz0yNDcwO2FwcGlkPXl0YWNoeW9u/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2021-05/6c1a9ec0-b815-11eb-8b33-87fbb637229f.cf.jpg",
              num_available: 3,
              description: "Tablet device",
              max_reservation_time: 3}]
  }
}
