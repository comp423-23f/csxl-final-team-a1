import { TestBed } from '@angular/core/testing';

import { AdminEquipmentService } from './admin-equipment.service';

describe('AdminEquipmentService', () => {
  let service: AdminEquipmentService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AdminEquipmentService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
