import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PersonalInfo } from '../../../models/curriculum.model';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './header.component.html'
})
export class HeaderComponent {
  @Input() info!: PersonalInfo;

  onImgError(event: Event) {
    (event.target as HTMLImageElement).src = 'assets/images/foto_rodrigo.jpg';
  }
}
