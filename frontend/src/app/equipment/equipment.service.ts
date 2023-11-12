import { Injectable } from '@angular/core';
import { HttpClient, HttpContext } from '@angular/common/http';
import { Observable, Subscription } from 'rxjs';
import EquipmentType from './equipment-type.model';
import { Profile } from '../models.module';
import { AuthenticationService } from '../authentication.service';
import { ProfileService } from '../profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export default class EquipmentService {
  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  constructor(
    private http: HttpClient,
    private auth: AuthenticationService,
    private profileService: ProfileService
  ) {
    this.profileSubscription = this.profileService.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  //Return equipment types requested from backend.
  getEquipmentTypes(): Observable<EquipmentType[]> {
    return this.http.get<EquipmentType[]>('/api/equipment/list-all-equipments');
  }

  getAgreementStatus(): Observable<boolean> {
    let pid: number = 0;
    let onyen: string = '';
    if (this.profile !== undefined) {
      pid = this.profile.pid;
      onyen = this.profile.onyen;
    }
    return this.http.get<boolean>(
      '/api/equipment/get-user-agreement-status/' + pid + '/' + onyen
    );
  }

  updateAgreementStatus(): Observable<boolean> {
    let pid: number = 0;
    let onyen: string = '';
    if (this.profile !== undefined) {
      pid = this.profile.pid;
      onyen = this.profile.onyen;
    }
    console.log('here');

    return this.http.put<boolean>(
      '/api/equipment/update-user-agreement-status',
      [pid, onyen]
    );
  }
}

/* {id: 2,
            title: "iPad",
            num_available: 3,
            img_url: "https://s.yimg.com/uu/api/res/1.2/vVXUm8VfTF7kLKvCIqrKjg--~B/Zmk9ZmlsbDtoPTEyNzA7dz0yNDcwO2FwcGlkPXl0YWNoeW9u/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2021-05/6c1a9ec0-b815-11eb-8b33-87fbb637229f.cf.jpg",
            description: "Tablet device",
            max_reservation_time: 3} */
