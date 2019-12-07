import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges,
  ViewChild
} from '@angular/core';
import { Document } from "../models/document.model";


@Component({
  selector: 'results',
  templateUrl: '../templates/results.component.html',
  styleUrls: ['../styles/results.component.scss']
})
export class ResultsComponent implements OnChanges, OnInit {
  @Input() public results: Document[] = [];
  @Input() public nSummaryWords: number;
  @Input() public nResults: number;
  @Output() public bottomReached: EventEmitter<boolean> = new EventEmitter<boolean>();
  public sortedResults: Document[] = [];

  @ViewChild('resultWrapper', {read: ElementRef, static: true}) public wrapper: ElementRef;
  @ViewChild('bottom', {read: ElementRef, static: true}) public bottom: ElementRef;

  getSummary(result: Document) {
    return result.summary[0] ? '<strong>Zusammenfassung</strong> (max. ' + this.nSummaryWords + ' Wörter): ' + result.summary[0].split(' ').slice(0, this.nSummaryWords).join(' ') : '';
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.sortedResults = this.results.sort(r => r.score)
  }

  ngOnInit(): void {
    let options = {
      root: this.wrapper.nativeElement,
      rootMargin: '0px',
      threshold: 1.0
    };
    let observer = new IntersectionObserver(() => {
      this.bottomReached.emit(true);
    }, options);

    observer.observe(this.bottom.nativeElement);
  }

}

