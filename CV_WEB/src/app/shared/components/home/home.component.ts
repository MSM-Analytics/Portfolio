import {
  Component,
  AfterViewInit
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { PersonalInfo, Curriculum } from '../../../models/curriculum.model';

import { generateCvPdf } from '../../pdf/cv-pdf.builder';
import { CardsComponent } from '../cards/cards.component';
import { cards } from '../../../features/home/card.data';
import { CardItem } from '../../../models/curriculum.model';

import { HOME_PERSONAL } from '../../../features/home/personal.data';
import { HOME_PROGRAMADOR } from '../../../features/home/programador.data';
import { HOME_ANALISTA } from '../../../features/home/analista.data';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, CardsComponent],
  templateUrl: './home.component.html'
})
export class HomeComponent implements AfterViewInit {

  constructor(private router: Router) { }

  // =========================
  // DADOS
  // =========================

  cards: CardItem[] = cards;
  programador = this.cards[0];
  analista = this.cards[1];

  personalData: Curriculum = HOME_PERSONAL;
  programadorData: Curriculum = HOME_PROGRAMADOR;
  analistaData: Curriculum = HOME_ANALISTA;

  info: PersonalInfo = HOME_PERSONAL.personalInfo;

  viewMode: 'home' | 'programador' | 'analista' = 'home';

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
  // IMAGE FALLBACK
  // =========================

  onImgError(event: Event) {
    (event.target as HTMLImageElement).src =
      'assets/images/foto_rodrigo.jpg';
  }

  // =========================
  // ABRIR CURRÍCULO
  // =========================

  abrirCurriculo(tipo: 'programador' | 'analista'): void {
    localStorage.setItem('viewMode', tipo);
    this.router.navigate(['/curriculo', tipo]);
  }

  // =========================
  // VOLTAR HOME
  // =========================

  voltarHome() {
    this.viewMode = 'home';
    localStorage.setItem('viewMode', 'home');
    window.scrollTo(0, 0);
  }

  // =========================
  // BAIXAR PDF
  // =========================

  baixarCv(data: Curriculum): void {
    const tipo =
      this.viewMode === 'programador'
        ? 'programador'
        : 'analista';

    generateCvPdf(data, tipo);
  }

  // =========================
  // PORTFÓLIO
  // =========================

  abrirPortfolio(tipo: string) {
    this.router.navigate([`/portfolio/${tipo}`]);
  }

  // =========================
  // IDADE
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