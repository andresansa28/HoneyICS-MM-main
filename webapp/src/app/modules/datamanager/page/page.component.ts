import { Component } from '@angular/core';
import { FastAPIserviceService } from 'src/app/services/fast-apiservice.service';
import { NgxPermissionsService } from 'ngx-permissions';
import { AuthService } from 'src/app/shared/services/authService';
import { AnalyzerService } from 'src/app/services/analyzer.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-page',
  templateUrl: './page.component.html',
  styleUrls: ['./page.component.scss'],
})

export class PageComponent {
  loading:boolean = false;
  response?: string;

  constructor(
    private service:FastAPIserviceService,
    private permissionsService: NgxPermissionsService,
    private keycloakService: AuthService,
    private analyzerService: AnalyzerService,
    private _snackBar: MatSnackBar,
    ) { }

  async test(): Promise<any>{
    return new Promise((resolve,reject) =>{
      this.service.getPosts("ciao").subscribe(response => {
        resolve(response);
      });
    })
  }
  async getData(val:string): Promise<any>{
    return new Promise((resolve,reject) =>{
      this.service.uploadData(val).subscribe(response => {
        resolve(response);
      });
    })
  }

  async remData(val:string): Promise<any>{
    return new Promise((resolve,reject) =>{
      this.service.removeIndex(val).subscribe(response => {
        resolve(response);
      });
    })
  }

  async load(){
    this.loading = true;
    let data = await this.getData("zeekdata")
    this.response = data[0]
    this.loading = false;
  }

  async remove(){
    this.loading = true;
    let data = await this.remData("testindex")
    this.response = data[0]
    this.loading = false;
  }

  async testd(){
    this.loading = true;
    let data = await this.test()
    console.log(data)
    this.response = data[0]
    this.loading = false;
  }

  async load_json() {
    this.analyzerService.load_json().subscribe((res: any) => {
      console.log(res);
      if (res== 'Zeek run') {
        this._snackBar.open('Jsons loaded', 'Chiudi', {
          duration: 2000, // Durata in millisecondi
        });
      }
    });
  }

  async run_zeek() {
    this.analyzerService.run_zeek().subscribe((res: any) => {
      console.log(res);
      if(res == 'Jsons loaded'){
        this._snackBar.open('Zeek run', 'Chiudi', {
          duration: 2000, // Durata in millisecondi
        });
      }
    });
    
  }
}
