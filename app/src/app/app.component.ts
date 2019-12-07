import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { FormControl, FormGroup } from "@angular/forms";
import { Document } from './models/document.model';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'app';
  docs = [];

  public pageSize: number = 10;
  public results = [];
  public nResults: number = 0;
  public curPage: number = 1;
  public lastPageLoaded: number = 1;

  public query: {
    query: string,
    params: {
      topic?: string,
      date?: Date,
      nChars?: number[],
      nSummaryWords?: number
    }
  } = {query: '*', params: {}};

  public constructor(private http: HttpClient) {
  }

  public updateQueryParams(params: FormGroup) {
    this.query.params.topic = params.get('topic').value;
    this.query.params.date = params.get('date').value;
    this.query.params.nChars = [params.get('nCharsLo').value, params.get('nCharsHi').value];
    this.query.params.nSummaryWords = params.get('nSummaryWords').value;
    this.executeQuery();
  }

  public updateQuery(query: string) {
    this.query.query = query;
    this.executeQuery();
  }

  executeQuery(reset: boolean = true) {

    const doHighlight = this.query.query !== '*';

    if (reset) {
      this.curPage = 1;
      this.lastPageLoaded = 1;
      this.results = [];
    }

    const params = {
      'hl': doHighlight ? 'on' : 'off',
      'hl.fl': 'text',
      'fl': '*,score',
      'start': (this.curPage - 1) * this.pageSize,
      'rows': this.pageSize,
      'q': ''
    };


    const date = this.query.params.date;
    const filter = [];

    if (this.query.query) {
      filter.push('_text_:' + this.query.query);
    }
    if (this.query.params.topic) {
      filter.push('topic:' + this.query.params.topic);
    }
    if (this.query.params.date) {
      date.setHours(5);
      filter.push('text_dates:"' + date.toISOString().replace(/\d{2}:\d{2}:\d{2}.\d{3}/, '00:00:00.000') + '"');
    }
    if (this.query.params.nChars) {
      filter.push('text_length:[' + this.query.params.nChars[0] + ' TO ' + this.query.params.nChars[1] + ']');
    }

    params['q'] = filter.join(' AND ');

    const nonNullParams = {};
    for (const key in params) {
      if (params.hasOwnProperty(key) && params[key] !== null && params[key] !== undefined) {
        nonNullParams[key] = params[key];
      }
    }


    const url = new URL(location.href + 'solr/summaries/query');
    url.search = (new URLSearchParams(nonNullParams)).toString();


    this.http.get<{ response: any, highlighting: any }>(
      url.toString())
      .subscribe(resp => {
        this.nResults = resp.response.numFound;
        const start = resp.response.start;
        const results = resp.response.docs.map(d => {
          const doc = new Document();
          doc.text = d.text;
          doc.text_length = d.text_length;
          doc.topic = d.topic;
          doc.summary = d.summary;
          doc.nNouns = d.text_num_nouns;
          doc.nVerbs = d.text_num_verbs;
          doc.nDates = d.text_num_dates;
          doc.score = d.score;
          doc.highlights = doHighlight ? resp.highlighting[d.id].text : '';
          return doc;
        });

        if (start === 0 || start > (this.lastPageLoaded - 1) * this.pageSize) {
          this.lastPageLoaded = start / this.pageSize + 1;
          this.curPage = this.lastPageLoaded;
          this.results = this.results.concat(results);
        }
      })
  }

  ngOnInit(): void {


    this.executeQuery();
  }

  bottomReached() {
    this.curPage = this.lastPageLoaded + 1;
    this.executeQuery(false);
  }
}

