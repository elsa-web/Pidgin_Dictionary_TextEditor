import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-feature-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './feature-card.html',
  styleUrls: ['./feature-card.css']
})
export class FeatureCardComponent {
  @Input() icon: string = 'A';         // Single letter or emoji fallback
  @Input() iconSvg: string = '';       // SVG path data (optional)
  @Input() title: string = 'Feature';
  @Input() description: string = '';
  @Input() accentColor: string = '#1a8cff';  // Neon color for hover glow
}
