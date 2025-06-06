import {Injectable} from "@angular/core";
import {KeycloakService} from "keycloak-angular";
import {KeycloakProfile, KeycloakTokenParsed} from "keycloak-js";
import { NgxPermissionsService } from "ngx-permissions";

@Injectable()
export class AuthService {
  constructor(
    private keycloakService: KeycloakService,
    private permissionsService: NgxPermissionsService,
    ) {
  }

  public getLoggedUser(): KeycloakTokenParsed | undefined {
    try {
      const keycloakInstance = this.keycloakService.getKeycloakInstance();
      this.permissionsService.loadPermissions(this.getRoles())
      return keycloakInstance.idTokenParsed;
    } catch (e) {
      console.error("exception", e)
      return undefined;
    }
  }

  public isLoggedIn(): Promise<boolean> {
    return this.keycloakService.isLoggedIn();
  }

  public loadUserProfile(): Promise<KeycloakProfile> {
    return this.keycloakService.loadUserProfile();
  }

  public login(): void{
    this.keycloakService.login({
      redirectUri: window.location.origin
    });
  }
  public logout(): void{
    this.keycloakService.logout(window.location.origin);
  }
  public redirectToProfile(): void{
    this.keycloakService.getKeycloakInstance().accountManagement();
  }
  public getRoles(): string[]{
    return this.keycloakService.getUserRoles();
  }
  public getName(): string{
    return this.keycloakService.getUsername() 
  }
}
