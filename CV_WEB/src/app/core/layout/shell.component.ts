import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

import { HeaderComponent } from '../../shared/components/header/header.component';
import { HOME_DATA } from '../../features/home/home.data';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    HeaderComponent
  ],
  templateUrl: './shell.component.html'
})
export class ShellComponent {
  data = HOME_DATA;
}
