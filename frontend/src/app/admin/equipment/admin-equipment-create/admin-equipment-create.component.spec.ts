import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminEquipmentCreateComponent } from './admin-equipment-create.component';

describe('AdminEquipmentCreateComponent', () => {
  let component: AdminEquipmentCreateComponent;
  let fixture: ComponentFixture<AdminEquipmentCreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminEquipmentCreateComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminEquipmentCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
