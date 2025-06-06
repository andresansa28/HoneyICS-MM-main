import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DatamanagerRoutingModule } from './datamanager-routing.module';
import { PageComponent } from './page/page.component';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { NgxPermissionsModule } from 'ngx-permissions';
import { MatSnackBarModule } from '@angular/material/snack-bar';

@NgModule({
  declarations: [
    PageComponent
  ],
  imports: [
    CommonModule,
    DatamanagerRoutingModule,
    CardModule,
    ButtonModule,
    MatSnackBarModule,
    NgxPermissionsModule.forChild()
  ]
})
export class DatamanagerModule { }
