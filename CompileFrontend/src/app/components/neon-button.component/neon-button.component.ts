import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-neon-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './neon-button.component.html',
  styleUrls: ['./neon-button.component.css']
})
export class NeonButtonComponent {
  @Input() label: string = 'Button';
  @Input() variant: 'primary' | 'outline' = 'primary';
  @Output() clicked = new EventEmitter<void>();

  onClick() {
    this.clicked.emit();
  }
}