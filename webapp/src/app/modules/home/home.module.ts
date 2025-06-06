import {CommonModule} from '@angular/common';
import {NgModule} from '@angular/core';
import {HomeRoutingModule} from "./home-routing.module";
import {HomeComponent} from "./pages/dashboard/home.component";
import {CardModule} from "primeng/card";
import {NgxPermissionsModule} from 'ngx-permissions';

@NgModule({
  declarations: [HomeComponent],
  imports: [
    CommonModule,
    HomeRoutingModule,
    CardModule,
    NgxPermissionsModule.forChild()
  ],
})
export class HomeModule {
}
