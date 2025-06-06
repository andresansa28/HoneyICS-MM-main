import { TestBed } from '@angular/core/testing';

import { FastAPIserviceService } from './fast-apiservice.service';

describe('FastAPIserviceService', () => {
  let service: FastAPIserviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FastAPIserviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
