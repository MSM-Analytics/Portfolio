import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

import { HOME_PERSONAL } from '../../features/home/personal.data';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet
  ],
  templateUrl: './shell.component.html'
})
export class ShellComponent {
  data = HOME_PERSONAL;
}
