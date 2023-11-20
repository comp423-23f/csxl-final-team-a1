import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminEquipmentBaseComponent } from './admin-equipment-base.component';

describe('AdminEquipmentBaseComponent', () => {
  let component: AdminEquipmentBaseComponent;
  let fixture: ComponentFixture<AdminEquipmentBaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminEquipmentBaseComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminEquipmentBaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
