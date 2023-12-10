import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'calendar-square',
  templateUrl: './calendar-square.widget.html',
  styleUrls: ['./calendar-square.widget.css']
})
export class CalendarSquare {
  /** Inputs and Outputs */
  @Input() reserved!: boolean;

  @Output() selectButtonPressed = new EventEmitter<boolean>();

  selected: boolean = false;

  /** Constructor */
  constructor() {}

  click_tile() {
    this.selected = !this.selected;
    this.selectButtonPressed.emit(this.selected);
  }
}
