import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsermanagerRoutingModule } from './usermanager-routing.module';
import { PageComponent } from './page/page.component';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { NgxPermissionsModule } from 'ngx-permissions';
import {TableModule} from 'primeng/table';
import {PaginatorModule} from "primeng/paginator";
import {InputTextModule} from "primeng/inputtext";
import {MessagesModule} from "primeng/messages";
import {PanelMenuModule} from "primeng/panelmenu";
import {RadioButtonModule} from "primeng/radiobutton";
import {DialogModule} from "primeng/dialog";
import {RippleModule} from "primeng/ripple";
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    PageComponent
  ],
  imports: [
    CommonModule,
    UsermanagerRoutingModule,
    CardModule,
    ButtonModule,
    TableModule,
    NgxPermissionsModule.forChild(),
    PaginatorModule,
    InputTextModule,
    MessagesModule,
    PanelMenuModule,
    DialogModule,
    RippleModule,
    RadioButtonModule,
    FormsModule,
    ReactiveFormsModule
  ]
})
export class UsermanagerModule {}
