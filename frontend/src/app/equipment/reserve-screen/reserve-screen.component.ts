import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

import ItemDetails from '../item-details.model';
import EquipmentService from '../equipment.service';
import EquipmentType from '../type.model';

@Component({
  selector: 'app-reserve-screen',
  templateUrl: './reserve-screen.component.html',
  styleUrls: ['./reserve-screen.component.css']
})
export class ReserveScreenComponent {
  public static route = {
    path: 'reserve-screen/:type_id',
    component: ReserveScreenComponent,
    children: []
  };

  type_id: number;

  items: ItemDetails[];
  type: EquipmentType;
  dates: string[];

  selected_items_id: number[] = [];
  selected_dates: Date[] = [];

  constructor(
    private route: ActivatedRoute,
    private equipment_service: EquipmentService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    const routeParams = this.route.snapshot.paramMap;
    this.type_id = Number(routeParams.get('type_id'));

    this.items = this.equipment_service.getTypeAvailability(this.type_id);
    if (this.items.length === 0) {
      this.router.navigate(['/equipment-reservations']);
    }
    this.type = this.items[0].equipment_type;
    this.dates = Object.keys(this.items[0].availability);
  }

  toDate(d: string): Date {
    return new Date(d);
  }

  clickSquare(date: Date, item_id: number, selected: boolean): void {
    if (selected) {
      this.selected_items_id.push(item_id);
      this.selected_dates.push(date);
    } else {
      let id_i = this.selected_items_id.indexOf(item_id);
      let date_i = this.selected_dates.indexOf(date);

      this.selected_items_id.splice(id_i, 1);
      this.selected_dates.splice(date_i, 1);
    }
  }

  onSubmit(): void {
    // Make sure submit is not on no values
    if (this.selected_dates.length === 0) {
      this.snackBar.open('Please select dates to reserve', 'Ok', {
        duration: 5000
      });
      return;
    }
    // Test for only 1 item id in list
    for (let i = 1; i < this.selected_items_id.length; i++) {
      if (this.selected_items_id[0] !== this.selected_items_id[i]) {
        this.snackBar.open('Please reserve only 1 item', 'Ok', {
          duration: 5000
        });
        return;
      }
    }

    // Test that dates are consecutive
    this.selected_dates.sort((a, b) => {
      return a.getTime() - b.getTime();
    });
    for (let i = 1; i < this.selected_dates.length; i++) {
      if (
        this.selected_dates[i].getDate() - 1 !==
        this.selected_dates[i - 1].getDate()
      ) {
        this.snackBar.open('Please select consecuitive dates', 'Ok', {
          duration: 5000
        });
        return;
      }
    }
    // Send API call
  }
}
