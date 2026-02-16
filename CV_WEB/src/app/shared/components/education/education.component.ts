import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Education } from '../../../models/curriculum.model';

@Component({
  selector: 'app-education',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './education.component.html'
})
export class EducationComponent {
  @Input() education!: Education[];
}
