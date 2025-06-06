import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})


export class UsermanagmentApiService {
  private url = 'http://localhost:5000'

  constructor(private httpClient: HttpClient) { }

  getUsers(){
    return this.httpClient.get(this.url+"/users");
  }


  removeUser(id:string){
    let queryParams = new HttpParams();
    queryParams = queryParams.append("user_id",id)
    return this.httpClient.delete(this.url+"/user/delete/",{params:queryParams});
  }

  createUser(username:string, firstname: string, lastname: string, email: any, password: any){
    const headers = { 'Content-Type': 'application/json'}
    return this.httpClient.post(this.url+"/user/create/",
      {username: username,
        first_name:firstname,
        last_name:lastname,
        email:email,
        password:password
    },{ headers: headers });
  }

  getUserRoles(id:string){
    let queryParams = new HttpParams();
    queryParams = queryParams.append("user_id",id)
    return this.httpClient.get(this.url+"/user/group/",{params:queryParams});
  }

  getAllGroups() {
    return this.httpClient.get(this.url+"/groups");
  }

  setUserGroup(id:string,gid:string) {
    const headers = { 'Content-Type': 'application/json'}
    return this.httpClient.post(this.url+"/user/group/add/",
      {
        user_id: id,
        group_name:gid
      },{ headers: headers });  }
}
