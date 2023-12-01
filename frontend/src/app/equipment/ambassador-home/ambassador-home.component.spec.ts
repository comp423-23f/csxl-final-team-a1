import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AmbassadorHomeComponent } from './ambassador-home.component';

describe('AmbassadorHomeComponent', () => {
  let component: AmbassadorHomeComponent;
  let fixture: ComponentFixture<AmbassadorHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AmbassadorHomeComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AmbassadorHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
