import { HttpClient, HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AnalyzerService } from 'src/app/services/analyzer.service';
import { ConfigService } from 'src/app/services/config.service';
import { Container, DeployModel, DeploymentsModel } from 'src/app/shared/deploymentModels/deploymentsModel';

@Component({
  selector: 'app-deployment',
  templateUrl: './page.component.html',
  styleUrls: ['./page.component.scss']
})
export class DeploymentComponent implements OnInit{

  button_green: string = 'button_green';
  button_red: string = 'button_red';
  isDivActive: boolean = true;
  deployments: DeploymentsModel = {
    delay: 0,
    MaxMind_GeoDB_Key: '',
    RemoteDeployments: []
  };  
  delayValue: number = this.deployments.delay || 60;
  geoDbKey: string = '';

  //add deploy variables
  name_input: string = 'Deploy_test';
  IP_input: string = '192.168.1.10';
  user_input: string = 'admin';
  passw_input: string = 'admin';
  add_container_ip_input: string = '';
  add_container_name_input: string = '';
  Containers_input: Container[] = [];

  constructor(private http: HttpClient, private configS: ConfigService, private _snackBar: MatSnackBar, private analyzerS: AnalyzerService) {}
  
  ngOnInit(): void {
    // this.http.get('http://localhost:8080/ips').subscribe((res: any) => { 
    //   this.ips = res;
    // });
    this.initDeployments();
  }

  // async function to active div
  toggleDiv() {
    this.isDivActive = !this.isDivActive, 2000;
  }

  initDeployments(): void {
    this.configS.getDeployments().subscribe((res: any) => { 
      var remote: DeployModel[] = [];
      for (var i = 0; i < res.RemoteDeployments.length; i++) {
        var deploy: DeployModel = {
          name: res.RemoteDeployments[i].name,
          IP: res.RemoteDeployments[i].IP,
          user: res.RemoteDeployments[i].user,
          passw: res.RemoteDeployments[i].passw,
          active: true,
          Containers: res.RemoteDeployments[i].Containers
        };
        remote.push(deploy);
      }
      this.deployments = {
        delay : res.delay,
        MaxMind_GeoDB_Key : res.MaxMind_GeoDB_Key,
        RemoteDeployments : remote
      }
      this.delayValue = this.deployments.delay;
      this._snackBar.open('Dati aggiornati con successo!', 'Chiudi', {
        duration: 2000, // Durata in millisecondi
    });
  }, (error: any) => {
    this._snackBar.open('Errore nel caricamento dei dati!', 'Chiudi', {
      duration: 2000, // Durata in millisecondi
  });
});
}

  checkDeploymentsStatus(): void {
    this.configS.checkDeployments(this.deployments).subscribe((res: any) => { 
      // restituisce il deployModel degli ip che sono attivi
      console.log(res);
      
    }, 
    (error: any) => {
      this._snackBar.open('Errore nel caricamento dei dati!', 'Chiudi', {
        duration: 2000, // Durata in millisecondi
    });
  });
  }

  setDelayConfig(){
    this.configS.setDelayConfig(this.delayValue).subscribe((res: any) => { 
      if (res["message"] == "Delay changed successfully"){
        this.initDeployments();
      }
    },
    (error: any) => {
      this._snackBar.open('Errore nel caricamento dei dati!', 'Chiudi', {
        duration: 2000, // Durata in millisecondi
        });
      });
  }

  setKeyConfig(){
    this.configS.setKeyConfig(this.geoDbKey).subscribe((res: any) => { 
      console.log(res);
      if (res["message"] == "MaxMind_GeoDB_Key changed successfully"){
        this.initDeployments();
      }
    });
  }

  addDeployment(): void {
    var deploy: DeployModel = {
      name: this.name_input,
      IP: this.IP_input,
      user: this.user_input,
      passw: this.passw_input,
      active: true,
      Containers: this.Containers_input
    };

    this.configS.addDeployment(deploy).subscribe((res: any) => { 
    });
  }

  removeDeployment(ipToRemove: string): void {
    console.log(ipToRemove);
    this.configS.removeDeployment(ipToRemove).subscribe((res: any) => { 
      console.log(res);
      if (res["message"] == "Deployments added successfully"){
        this.initDeployments();
      } else {
        this._snackBar.open('Errore nell\'aggiunta del deployment!', 'Chiudi', {
          duration: 2000, // Durata in millisecondi
      });
      }
    });
  }

  onUpload(event: any): void {
    var response: HttpResponse<any> = event.originalEvent;
    console.log(response.body["message"]);

    for (const file of event.files) {
      console.log(file);
    }
  }

  startAnalyzer(): void {
    this.analyzerS.start().subscribe((res: any) => { 
      console.log(res);
    });
  }

  stopAnalyzer(): void {
    this.analyzerS.stop().subscribe((res: any) => { 
      console.log(res);
    });
  }

  forceOpenSearchSetup(): void {
    this.analyzerS.forceOpenSearchSetup().subscribe((res: any) => { 
      console.log(res);
      if (res == "Opensearch configured"){
        this._snackBar.open('OpenSearch setup configured successfully!', 'Chiudi', {
          duration: 2000, // Durata in millisecondi
      });
      }
    });
  }

  addPlcIp(): void {
    if (this.add_container_ip_input == '') {
      return;
    }
    var container: Container = {
      IP: this.add_container_ip_input,
      name: this.add_container_name_input
    };
    this.Containers_input.push(container);
  }

}