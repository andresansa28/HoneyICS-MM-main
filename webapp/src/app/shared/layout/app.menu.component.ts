import {OnInit} from '@angular/core';
import {Component} from '@angular/core';
import {LayoutService} from './service/app.layout.service';


@Component({
  selector: 'app-menu',
  templateUrl: './app.menu.component.html'
})
export class AppMenuComponent implements OnInit {

  model: any[] = [];

  constructor(public layoutService: LayoutService) {
  }

  ngOnInit() {

    this.model = [
      {
        label: 'Home',
        items: [
          //https://primeng.org/icons
          {label: 'Dashboard', icon: 'pi pi-fw pi-home', routerLink: ['/'], permission:['admin','Analyst']},
          {label: 'Data Manager', icon: 'pi pi-fw pi-database', routerLink: ['/datamanager'], permission:['admin']},
          {label: 'User Manager', icon: 'pi pi-fw pi-users', routerLink: ['/usermanager'], permission:['admin']},
          {label: 'Deployment', icon: 'pi pi-fw pi-cloud', routerLink: ['/deployment'], permission:['admin']},
        ]
      },
    ]
  }
}
