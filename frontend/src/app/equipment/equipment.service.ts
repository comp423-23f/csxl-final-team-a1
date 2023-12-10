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
}
