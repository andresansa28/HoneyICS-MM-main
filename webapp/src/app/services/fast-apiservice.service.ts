import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})


export class FastAPIserviceService {
  private url = 'http://localhost:5000'

  constructor(private httpClient: HttpClient) { }

  getPosts(value:string){
    let queryParams = new HttpParams();
    queryParams = queryParams.append("sf",value)
    return this.httpClient.get(this.url+"/test");
  }


  uploadData(index_name:string){
    let queryParams = new HttpParams();
    queryParams = queryParams.append("index_name",index_name)
    return this.httpClient.get(this.url+"/loadcsv/",{params:queryParams});
  }

  removeIndex(index_name:string){
    let queryParams = new HttpParams();
    queryParams = queryParams.append("index_name",index_name)
    return this.httpClient.get(this.url+"/rmIndex/",{params:queryParams});
  }
}
