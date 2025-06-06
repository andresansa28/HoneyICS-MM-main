import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AnalyzerService {
  url: string = "http://172.17.0.1:5003";
  constructor(private http: HttpClient) { }

  start() {
    return this.http.get(`${this.url}/start`);
  }

  stop() {
    return this.http.get(`${this.url}/stop`);
  }

  forceOpenSearchSetup() {
    return this.http.get(`${this.url}/force_opensearch_config`);
  }

  load_json() {
    return this.http.get(`${this.url}/load_json`);
  }

  run_zeek() {
    return this.http.get(`${this.url}/run_zeek?standard=False`);
  }
}
