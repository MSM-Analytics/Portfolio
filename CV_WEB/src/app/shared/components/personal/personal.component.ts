import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-personal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './personal.component.html'
})
export class PersonalComponent {
  @Input() summary!: string;
}