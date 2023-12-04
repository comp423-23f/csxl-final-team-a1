import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'calendar-square',
  templateUrl: './calendar-square.widget.html',
  styleUrls: ['./calendar-square.widget.css']
})
export class CalendarSquare {
  /** Inputs and Outputs */
  @Input() date!: Date;
  @Input() reserved!: boolean;

  @Output() selectButtonPressed = new EventEmitter<Date>();

  selected: boolean = false;

  /** Constructor */
  constructor() {}

  click_tile() {
    this.selected = !this.selected;
    this.selectButtonPressed.emit(this.date);
  }
}
