import { Routes } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page/landing-page';
import { EditorPageComponent } from './editor-page/editor-page/editor-page';

export const routes: Routes = [
  { path: '',        component: LandingPageComponent },
  { path: 'editor',  component: EditorPageComponent  },
  { path: '**',      redirectTo: ''                  }
];