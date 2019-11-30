import { Component } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';
  docs = [];

  public constructor(private http: HttpClient) {

    http.get<{response: any}>('/solr/mycore/query?q='+encodeURIComponent('*:*')).subscribe(resp => {
      this.docs = resp.response.docs.map(d => JSON.stringify(d));
    })
  }
}

