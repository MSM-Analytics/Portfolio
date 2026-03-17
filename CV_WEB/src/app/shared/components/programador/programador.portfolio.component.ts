import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { PORTFOLIO_DATA_JS } from '../../../features/home/programador.portfolio.data';
import { DataPortfolioItem } from '../../../models/curriculum.model';

@Component({
  selector: 'app-portfolio-programador',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './programador.portfolio.component.html'
})
export class PortfolioDevComponent {

  projects: DataPortfolioItem[] = PORTFOLIO_DATA_JS;

  trackById(index: number, item: DataPortfolioItem): string {
    return item.id;
  }

}