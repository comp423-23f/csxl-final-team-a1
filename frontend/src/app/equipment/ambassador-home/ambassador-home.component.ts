import { Component } from '@angular/core';
import { Route } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';

@Component({
  selector: 'app-ambassador-home',
  templateUrl: './ambassador-home.component.html',
  styleUrls: ['./ambassador-home.component.css']
})
export class AmbassadorHomeComponent {
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorHomeComponent,
    title: 'XL Equipment',
    canActivate: [permissionGuard('equipment.reservation.*', 'equipment')],
    resolve: { profile: profileResolver }
  };


}
