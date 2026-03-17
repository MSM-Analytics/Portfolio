import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cards.component.html'
})
export class CardsComponent {

  @Input() titulo!: string;
  @Input() descricao!: string;
  @Input() imagem!: string;
  @Input() invertido = false;
  @Input() tipo!: 'programador' | 'analista';

  @Output() abrir = new EventEmitter<'programador' | 'analista'>();

  @Output() abrirPortfolio = new EventEmitter<string>();

  abrirCurriculo() {
    this.abrir.emit(this.tipo);
  }

  abrirPortfolioClick() {
    this.abrirPortfolio.emit(this.tipo);
  }
}