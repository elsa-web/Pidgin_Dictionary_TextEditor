import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FontSelector } from './font-selector';

describe('FontSelector', () => {
  let component: FontSelector;
  let fixture: ComponentFixture<FontSelector>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FontSelector]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FontSelector);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
