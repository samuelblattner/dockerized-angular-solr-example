import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { HttpClientModule } from "@angular/common/http";
import { MatCardModule } from "@angular/material/card";
import { MatIconModule } from "@angular/material/icon";
import { MatInputModule, MatSelectModule, MatSliderModule, MatToolbarModule } from "@angular/material";
import { ReactiveFormsModule } from "@angular/forms";

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { HeaderComponent } from "./components/header.component";
import { FilterComponent } from "./components/filter.component";
import { MatExpansionModule } from "@angular/material/expansion";
import { ResultsComponent } from "./components/results.component";
import { MatDatepickerModule } from "@angular/material/datepicker";
import { MatNativeDateModule } from "@angular/material/core";
import { Ng5SliderModule } from "ng5-slider";
import { MatChipsModule } from "@angular/material/chips";


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FilterComponent,
    ResultsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MatInputModule,
    MatToolbarModule,
    MatSelectModule,
    MatSliderModule,
    ReactiveFormsModule,
    MatCardModule,
    MatIconModule,
    BrowserAnimationsModule,
    MatExpansionModule,
    MatDatepickerModule,
    MatNativeDateModule,
    Ng5SliderModule,
    MatChipsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}

