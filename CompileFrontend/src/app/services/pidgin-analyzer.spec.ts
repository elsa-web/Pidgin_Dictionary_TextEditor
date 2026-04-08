import { TestBed } from '@angular/core/testing';

import { PidginAnalyzer } from './pidgin-analyzer';

describe('PidginAnalyzer', () => {
  let service: PidginAnalyzer;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PidginAnalyzer);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
