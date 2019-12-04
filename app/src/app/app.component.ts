import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {FormControl, FormGroup} from "@angular/forms";
import {Document} from './models/document.model';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';
  docs = [];

  public results = [];

  public query: {
    query: string,
    params: {
      topic?: string,
      date?: Date,
      numChars?: number,
      numSummaryWords?: number
    }
  } = {query: '', params: {}};


  public constructor(private http: HttpClient) {
  }

  public updateQueryParams(params: FormGroup) {
    this.query.params.topic = params.get('topic').value;
    this.query.params.date = params.get('date').value;
    this.query.params.numChars = params.get('numChars').value;
    this.query.params.numSummaryWords = params.get('numSummarywords').value;
    this.executeQuery();
  }

  public updateQuery(query: string) {
    this.query.query = query;
    this.executeQuery();
  }

  executeQuery() {

    this.http.get<{ response: any, highlighting: any }>('/solr/summaries/query?hl=on&hl.fl=text&q=' + encodeURIComponent('_text_:' + this.query.query))
      .subscribe(resp => {
        this.results = resp.response.docs.map(d => {
          const doc = new Document();
          doc.text = d.text;
          doc.summary = d.summary;
          doc.nNouns = d.text_num_nouns;
          doc.nVerbs = d.text_num_verbs;
          doc.highlights = resp.highlighting[d.id].text;
          return doc;
        });
    })
  }
}

