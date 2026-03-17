import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { Curriculum } from '../../../models/curriculum.model';
import { HOME_ANALISTA } from '../../../features/home/analista.data';
import { generateCvPdf } from '../../pdf/cv-pdf.builder';

@Component({
  selector: 'app-analista',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analista.component.html'
})
export class AnalistaComponent {

  data: Curriculum = HOME_ANALISTA;

  constructor(private router: Router) {}

  voltar(): void {
    this.router.navigate(['/']);
  }

  baixar(): void {
    generateCvPdf(this.data, 'analista');
  }

}