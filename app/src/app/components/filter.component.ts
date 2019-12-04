import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormControl, FormGroup } from "@angular/forms";


@Component({
  selector: 'filter',
  templateUrl: '../templates/filter.component.html',
  styleUrls: ['../styles/filter.component.scss']
})
export class FilterComponent implements OnInit {

  public filterForm: FormGroup;

  @Output() public filterChanged: EventEmitter<FormGroup> = new EventEmitter<FormGroup>();

  ngOnInit(): void {
    this.filterForm = new FormGroup({
      topic: new FormControl(),
      query: new FormControl(),
      day: new FormControl(),
      month: new FormControl(),
      year: new FormControl(),
      nChars: new FormControl(),
      summaryWordCount: new FormControl()
    });

    this.filterForm.valueChanges.subscribe(() => this.filterChanged.emit(this.filterForm));
  }
}
