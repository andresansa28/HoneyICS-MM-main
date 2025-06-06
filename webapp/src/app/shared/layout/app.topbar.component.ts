import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MenuItem} from 'primeng/api';
import {LayoutService} from "./service/app.layout.service";
import {KeycloakService} from "keycloak-angular";
import { AuthService } from '../services/authService';
import { KeycloakProfile, KeycloakTokenParsed } from 'keycloak-js';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-topbar',
  templateUrl: './app.topbar.component.html'
})
export class AppTopBarComponent implements OnInit {

  items!: MenuItem[];
  
  name! : string;

  @ViewChild('menubutton') menuButton!: ElementRef;

  @ViewChild('topbarmenubutton') topbarMenuButton!: ElementRef;

  @ViewChild('topbarmenu') menu!: ElementRef;

  constructor(public layoutService: LayoutService,
    private keycloakService: KeycloakService,
    private authService: AuthService,
  
    ) {
  }
  
  ngOnInit(): void {
    const k : KeycloakTokenParsed = this.authService.getLoggedUser()!;
    this.name = k['preferred_username'];
  }
  
  logout() {
    this.keycloakService.logout(window.location.origin)
  }
  
  showUserData(){
    
  }
 
}
