import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminEquipmentEditComponent } from './admin-equipment-edit.component';

describe('AdminEquipmentEditComponent', () => {
  let component: AdminEquipmentEditComponent;
  let fixture: ComponentFixture<AdminEquipmentEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminEquipmentEditComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminEquipmentEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
