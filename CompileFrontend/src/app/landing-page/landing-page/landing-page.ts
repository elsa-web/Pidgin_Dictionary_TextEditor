import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { NeonButtonComponent } from '../../components/neon-button.component/neon-button.component';
import { FeatureCardComponent } from '../../components/feature-card/feature-card';

@Component({
  selector: 'app-landing-page',
  standalone: true,
  imports: [CommonModule, RouterLink, NeonButtonComponent, FeatureCardComponent],
  templateUrl: './landing-page.html',
  styleUrls: ['./landing-page.css']
})
export class LandingPageComponent {

  constructor(private router: Router) {}

  features = [
    {
      icon: 'A',
      iconSvg: 'M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z',
      title: 'Spelling Detection',
      description: 'Highlights misspelled words with red underlines and suggests corrections in real-time.',
      accentColor: '#ff4d6d'
    },
    {
      icon: 'S',
      iconSvg: 'M3 6h18M3 12h18M3 18h18',
      title: 'Syntax Analysis',
      description: 'Detects grammar structure violations in Pidgin English with blue underlines.',
      accentColor: '#1a8cff'
    },
    {
      icon: 'B',
      iconSvg: 'M4 19.5A2.5 2.5 0 016.5 17H20M4 4.5A2.5 2.5 0 016.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15z',
      title: 'Semantic Checking',
      description: 'Identifies words used in the wrong context and suggests more natural Pidgin alternatives.',
      accentColor: '#00e5a0'
    },
    {
      icon: 'D',
      iconSvg: 'M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12',
      title: 'Document Import',
      description: 'Upload .txt or .doc files and instantly analyze them for errors and corrections.',
      accentColor: '#a78bfa'
    },
    {
      icon: 'L',
      iconSvg: 'M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z',
      title: 'Live Text Editor',
      description: 'Type freely in the editor and get instant feedback with color-coded error highlighting.',
      accentColor: '#f59e0b'
    },
    {
      icon: 'P',
      iconSvg: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z',
      title: 'Pidgin Dictionary',
      description: 'Built-in word mapping from Standard English to Pidgin with 500+ entries.',
      accentColor: '#06b6d4'
    }
  ];

  openEditor() {
    this.router.navigate(['/editor']);
  }

  uploadDocument() {
    this.router.navigate(['/editor']);
  }
}