import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReserveScreenComponent } from './reserve-screen.component';

describe('ReserveScreenComponent', () => {
  let component: ReserveScreenComponent;
  let fixture: ComponentFixture<ReserveScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReserveScreenComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReserveScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
