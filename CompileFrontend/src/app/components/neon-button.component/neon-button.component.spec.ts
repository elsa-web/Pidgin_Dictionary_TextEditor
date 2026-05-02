import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NeonButtonComponent } from './neon-button.component';

describe('NeonButtonComponent', () => {
  let component: NeonButtonComponent;
  let fixture: ComponentFixture<NeonButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NeonButtonComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NeonButtonComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
