import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { Curriculum } from '../../../models/curriculum.model';
import { HOME_PROGRAMADOR } from '../../../features/home/programador.data';
import { generateCvPdf } from '../../pdf/cv-pdf.builder';

@Component({
  selector: 'app-programador',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './programador.component.html'
})
export class ProgramadorComponent {

  data: Curriculum = HOME_PROGRAMADOR;

  constructor(private router: Router) {}

  // voltar para home
  voltar(): void {
    this.router.navigate(['/']);
  }

  // baixar pdf
  baixar(): void {
    generateCvPdf(this.data, 'programador');
  }

}