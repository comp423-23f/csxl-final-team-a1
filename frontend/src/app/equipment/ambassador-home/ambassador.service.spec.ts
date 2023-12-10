import { TestBed } from '@angular/core/testing';

import { AmbassadorService } from './ambassador.service';

describe('AmbassadorService', () => {
  let service: AmbassadorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AmbassadorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
