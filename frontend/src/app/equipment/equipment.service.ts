import { Injectable } from '@angular/core';
import { HttpClient, HttpContext } from '@angular/common/http';
import { Observable, Subscription } from 'rxjs';
import TypeDetails from './equipment-type.model';
import { Profile } from '../models.module';
import { AuthenticationService } from '../authentication.service';
import { ProfileService } from '../profile/profile.service';
import ItemDetails from './item-details.model';

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
  getEquipmentTypes(): Observable<TypeDetails[]> {
    return this.http.get<TypeDetails[]>('/api/equipment/list-all-equipments');
  }

  getAgreementStatus(): Observable<boolean> {
    let pid: number = 0;
    if (this.profile !== undefined) {
      pid = this.profile.pid;
    }
    return this.http.get<boolean>(
      '/api/equipment/get-user-agreement-status/' + pid
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

  getTypeAvailability(type_id: number): ItemDetails[] {
    return [
      {
        id: 1,
        display_status: true,
        equipment_type: {
          id: 1,
          title: 'Quest 2',
          num_available: 1,
          img_url: 'Bla',
          description: 'Quest 2 go crazy fr',
          max_reservation_time: 3
        },
        availability: {
          '12-4-2023': true,
          '12-5-2023': false,
          '12-6-2023': false,
          '12-7-2023': true,
          '12-8-2023': true,
          '12-9-2023': true,
          '12-10-2023': true
        }
      }
    ];
  }
}
