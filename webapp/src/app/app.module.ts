import {APP_INITIALIZER, NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {AppLayoutModule} from "./shared/layout/app.layout.module";
import {KeycloakAngularModule, KeycloakService} from "keycloak-angular";
import {AuthService} from "./shared/services/authService";
import { NgxPermissionsModule } from 'ngx-permissions';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

function initializeKeycloak(keycloak: KeycloakService) {
  return () =>
    keycloak.init({
      config: {
        realm: "ICSConsole",
        url: "https://172.17.0.1:8443/auth",
        clientId: "webapp"
      },
    
      initOptions: {
        pkceMethod: 'S256',
        // must match to the configured value in keycloak
        redirectUri: 'http://localhost:5002',
        // this will solved the error
        checkLoginIframe: false
      }
    });
}
@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    KeycloakAngularModule,
    AppLayoutModule,
    AppRoutingModule,
    NgxPermissionsModule.forRoot(),
    BrowserAnimationsModule
  ],
  providers: [
    {
      provide: APP_INITIALIZER,
      useFactory: initializeKeycloak,
      multi: true,
      deps: [KeycloakService]
    },
    AuthService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
