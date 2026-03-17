import {
  Component,
  Input,
  Output,
  EventEmitter,
  AfterViewInit
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { PersonalInfo } from '../../../models/curriculum.model';
import { Curriculum } from '../../../models/curriculum.model';

import { generateCvPdf } from '../../pdf/cv-pdf.builder';
import { CardsComponent } from '../cards/cards.component';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, CardsComponent],
  templateUrl: './header.component.html'
})

export class HeaderComponent implements AfterViewInit {

  // =========================
  // INPUTS
  // =========================

  @Input() info!: PersonalInfo;
  @Input() data!: Curriculum;
  @Input() viewMode: 'home' | 'programador' | 'analista' = 'home';

  // =========================
  // OUTPUTS
  // =========================

  @Output() scrollClick = new EventEmitter<void>();
  @Output() voltarHomeClick = new EventEmitter<void>();

  constructor(private router: Router) { }

  // =========================
  // IMAGE FALLBACK
  // =========================

  onImgError(event: Event) {
    (event.target as HTMLImageElement).src =
      'assets/images/foto_rodrigo.jpg';
  }

  // =========================
  // LOAD ANIMATION
  // =========================

  isLoaded = false;

  ngAfterViewInit() {
    setTimeout(() => {
      this.isLoaded = true;
    }, 50);
  }

  // =========================
  // SCROLL
  // =========================

  onScrollClick(): void {
    this.scrollClick.emit();
  }

  // =========================
  // VOLTAR HOME
  // =========================

  voltarHome(): void {
    this.voltarHomeClick.emit();
    localStorage.setItem('viewMode', 'home');
    window.scrollTo(0, 0);
  }

  // =========================
  // ABRIR CV
  // =========================

  abrirCurriculo(tipo: 'programador' | 'analista'): void {
    localStorage.setItem('viewMode', tipo);
    window.scrollTo(0, 0);
  }

  // =========================
  // BAIXAR CV
  // =========================

  baixarCv(): void {
    const tipo =
      this.viewMode === 'programador' ? 'programador' : 'analista';

    generateCvPdf(this.data, tipo);
  }

  // =========================
  // ABRIR PORTFOLIO
  // =========================

  abrirPortfolio(tipo: string) {
    this.router.navigate([`/portfolio/${tipo}`]);
  }

  // =========================
  // CALCULAR IDADE
  // =========================

  calculateAge(birthDate?: string): number | null {
    if (!birthDate) return null;

    const today = new Date();
    const birth = new Date(birthDate);

    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (
      monthDiff < 0 ||
      (monthDiff === 0 && today.getDate() < birth.getDate())
    ) {
      age--;
    }

    return age;
  }

  get age(): number | null {
    return this.calculateAge(this.info?.birthDate);
  }
}