import { Routes } from '@angular/router';
import { HomeComponent } from './shared/components/home/home.component';
import { ProgramadorComponent } from './shared/components/programador/programador.component';
import { AnalistaComponent } from './shared/components/analista/analista.component';
import { PortfolioAnaliseComponent } from './shared/components/analista/analista.portfolio.component';
import { PortfolioDevComponent } from './shared/components/programador/programador.portfolio.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },

  { path: 'curriculo/programador', component: ProgramadorComponent },

  { path: 'curriculo/analista', component: AnalistaComponent },

  { path: 'portfolio/analista', component: PortfolioAnaliseComponent },

  { path: 'portfolio/programador', component: PortfolioDevComponent },

  {
    path: 'projeto/:id',
    loadComponent: () =>
      import('./shared/components/projects/project-view.component')
        .then(m => m.ProjectViewComponent)
  },

  { path: '**', redirectTo: '' }

];