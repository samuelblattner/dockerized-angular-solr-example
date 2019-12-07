import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from "@angular/forms";
import { LabelType, Options } from "ng5-slider";


@Component({
  selector: 'filter',
  templateUrl: '../templates/filter.component.html',
  styleUrls: ['../styles/filter.component.scss']
})
export class FilterComponent implements OnInit {

  public filterForm: FormGroup;
  public nCharsLow: number = 0;
  public nCharsHi: number = 5000;
  public nSummaryWords: number = 1000;

  options: Options = {
    floor: 0,
    ceil: 5000,
    translate: (value: number, label: LabelType): string => {
      switch (label) {
        case LabelType.Low:
          return '<b>Min. Zeichen:</b> ' + value;
        case LabelType.High:
          return '<b>Max Zeichen:</b> ' + value;
        default:
          return '$' + value;
      }
    }
  };

  public topics: string[] = [
    '---',
    'Wissenschaft & Technik',
    'Fussball',
    'Bildung',
    'Familie',
    'Dynastien',
    'Verkehr',
    'Geografie',
    'Adel',
    'Schiffahrt',
    'Sport',
    'Botanik',
    'Geschichte',
    'Musik',
    'Film',
    'Könige',
    'Kirchen',
    'Politik',
    'Hockey',
    'Krieg',
    'Deutschland'
  ];

  @Output() public filterChanged: EventEmitter<FormGroup> = new EventEmitter<FormGroup>();

  private emitValues() {
    // this.filterForm.setValue({'nCharsLo': this.nCharsLow});
    this.filterForm.get('nCharsLo').setValue(this.nCharsLow, {emitEvent: false});
    this.filterForm.get('nCharsHi').setValue(this.nCharsHi, {emitEvent: false});
    this.filterForm.get('nSummaryWords').setValue(this.nSummaryWords, {emitEvent: false});
    this.filterChanged.emit(this.filterForm)
  }

  ngOnInit(): void {
    this.filterForm = new FormGroup({
      topic: new FormControl(),
      date: new FormControl(),
      nCharsLo: new FormControl(),
      nCharsHi: new FormControl(),
      nSummaryWords: new FormControl()
    });

    this.filterForm.valueChanges.subscribe(() => {
      this.emitValues();
    });
  }
}
