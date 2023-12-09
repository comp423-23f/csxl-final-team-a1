import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { Route } from '@angular/router';
import { Observable, Subscription, map, tap, timer } from 'rxjs';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import EquipmentReservation from '../equipment-reservation.model';
import { AmbassadorService } from './ambassador.service';
import { EquipmentReservationDetails } from '../equipment-reservation.model';
import {
  MAT_SNACK_BAR_DATA,
  MatSnackBar,
  MatSnackBarRef
} from '@angular/material/snack-bar';

@Component({
  selector: 'app-ambassador-home',
  templateUrl: './ambassador-home.component.html',
  styleUrls: ['./ambassador-home.component.css']
})
export class AmbassadorHomeComponent implements OnInit, OnDestroy {
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorHomeComponent,
    title: 'XL Equipment',
    canActivate: [permissionGuard('equipment.reservation.*', 'equipment')],
    resolve: { profile: profileResolver }
  };

  reservations$: Observable<EquipmentReservationDetails[]>;
  upcomingReservations$: Observable<EquipmentReservationDetails[]>;
  activeReservations$: Observable<EquipmentReservationDetails[]>;
  pastReservations$: Observable<EquipmentReservationDetails[]>;

  columnsToDisplay = [
    'id',
    'name',
    'type',
    'item_id',
    'check_out_date',
    'expected_end_date',
    'actions'
  ];

  columnsToDisplayActive = [
    'id',
    'name',
    'type',
    'item_id',
    'check_out_date',
    'expected_end_date',
    'actions',
    'additional_info'
  ];

  columnsToDisplayPast = [
    'id',
    'name',
    'type',
    'item_id',
    'check_out_date',
    'expected_end_date',
    'actual_end_date',
    'return_description'
  ];

  private refreshSubscription!: Subscription;

  constructor(
    public ambassadorService: AmbassadorService,
    private _snackBar: MatSnackBar
  ) {
    this.reservations$ = this.ambassadorService.reservations$;
    this.upcomingReservations$ = this.reservations$.pipe(
      map((reservations) =>
        reservations.filter(
          (r) => !r.ambassador_check_out && r.actual_return_date === null
        )
      )
    );
    this.activeReservations$ = this.reservations$.pipe(
      map((reservations) =>
        reservations.filter(
          (r) => r.ambassador_check_out && r.actual_return_date === null
        )
      )
    );
    this.pastReservations$ = this.reservations$.pipe(
      map((reservations) =>
        reservations.filter((r) => r.actual_return_date !== null)
      )
    );
  }

  returnReservation(reservation: EquipmentReservationDetails): void {
    console.log(reservation.additional_description);
    let new_description = `${
      reservation.return_description
    }${new Date().toDateString()}: ${reservation.additional_description}`;
    this.ambassadorService.returnReservation(reservation, new_description);
  }

  ngOnDestroy(): void {
    this.refreshSubscription.unsubscribe();
  }

  ngOnInit(): void {
    this.refreshSubscription = timer(0, 5000)
      .pipe(tap((_) => this.ambassadorService.getEquipmentReservations()))
      .subscribe();
  }

  onBlur(): void {
    this.refreshSubscription = timer(0, 5000)
      .pipe(tap((_) => this.ambassadorService.getEquipmentReservations()))
      .subscribe();
  }

  onFocus(): void {
    this.refreshSubscription.unsubscribe();
  }

  openSnackBar(message: string) {
    let descriptionArray = message.split('\n');
    this._snackBar.openFromComponent(DescriptionComponent, {
      data: descriptionArray
    });
  }
}

@Component({
  selector: 'snack-bar',
  template:
    '<p *ngIf="data[0].length === 0">Nothing here...</p> <p *ngFor="let line of data;"> {{ line }} </p> <button mat-raised-button color = "accent" (click)="snackBarRef.dismiss()" style="display:flex; justify-content:flex; width:100%; padding:0;">Close</button>'
})
export class DescriptionComponent {
  constructor(
    public snackBarRef: MatSnackBarRef<DescriptionComponent>,
    @Inject(MAT_SNACK_BAR_DATA) public data: any
  ) {}
}
