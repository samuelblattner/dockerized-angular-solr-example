import { Component, Input } from '@angular/core';
import { Document } from "../models/document.model";


@Component({
  selector: 'results',
  templateUrl: '../templates/results.component.html',
  styleUrls: ['../styles/results.component.scss']
})
export class ResultsComponent {
  @Input() public results: Document[] = [];
}

