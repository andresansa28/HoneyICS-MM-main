import { TestBed } from '@angular/core/testing';

import { UsermanagmentAPIService } from './usermanagment-api.service';

describe('UsermanagmentAPIService', () => {
  let service: UsermanagmentAPIService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UsermanagmentAPIService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
