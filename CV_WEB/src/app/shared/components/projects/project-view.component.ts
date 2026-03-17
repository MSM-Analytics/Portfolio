import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-project-view',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './project-view.component.html'
})
export class ProjectViewComponent {

  projectUrl!: SafeResourceUrl;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer
  ) {

    const id = this.route.snapshot.paramMap.get('id');

    const url = `/assets/projects/${id}/index.html`;

    this.projectUrl =
      this.sanitizer.bypassSecurityTrustResourceUrl(url);

  }

}