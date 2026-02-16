import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HOME_DATA } from '../home/home.data';
import { AboutComponent } from '../../shared/components/about/about.component';
import { ExperienceComponent } from '../../shared/components/experience/experience.component';
import { EducationComponent } from '../../shared/components/education/education.component';
import { SkillsComponent } from '../../shared/components/skills/skills.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    AboutComponent,
    ExperienceComponent,
    EducationComponent,
    SkillsComponent
  ],
  templateUrl: './home.component.html'
})
export class HomeComponent {
  data = HOME_DATA;
}
