import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormControl } from "@angular/forms";


@Component({
  selector: 'header-component',
  templateUrl: '../templates/header.component.html',
  styleUrls: ['../styles/header.component.scss']
})
export class HeaderComponent implements OnInit {

  public queryInput: FormControl = new FormControl();

  @Output() public queryInputChanged: EventEmitter<string> = new EventEmitter<string>();

  ngOnInit(): void {
    this.queryInput.valueChanges.subscribe(() => {
      this.queryInputChanged.emit(this.queryInput.value);
    })
  }
}


