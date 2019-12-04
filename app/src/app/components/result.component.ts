import {Component, Input} from "@angular/core";
import {Document} from '../models/document.model';


@Component({
  selector: 'result',
  templateUrl: '../templates/result.component.html',
  styleUrls: ['../styles/result.component.scss']
})
export class ResultComponent {

  @Input() document: Document;
}

