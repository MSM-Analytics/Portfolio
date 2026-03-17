import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PORTFOLIO_DATA } from '../../../features/home/analista.portfolio.data';
import { DataPortfolioItem } from '../../../models/curriculum.model';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-portfolio-analise',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './analista.portfolio.component.html'
})
export class PortfolioAnaliseComponent {

  projects: DataPortfolioItem[] = PORTFOLIO_DATA;

  trackById(index: number, item: DataPortfolioItem): string {
    return item.id;
  }

}