import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {ProvaOggetto} from "./models/dataChart.dto";
import {KeycloakService} from "keycloak-angular";
import {AuthService} from "../../../../shared/services/authService";
import {KeycloakProfile, KeycloakTokenParsed} from "keycloak-js";



@Component({
  selector: 'app-dashboard',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  qualcosa!: string;
  provaOggetto: ProvaOggetto[] = [];
  user!: KeycloakTokenParsed | undefined;
  roles!: string;
  name! : string;

  constructor(
    private _router: Router,
    private keycloakService: AuthService,
  ) {
  }

  async ngOnInit() {

  }

}
