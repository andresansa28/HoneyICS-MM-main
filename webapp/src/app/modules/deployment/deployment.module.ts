import {CommonModule} from '@angular/common';
import {NgModule} from '@angular/core';
import {NgxPermissionsModule} from 'ngx-permissions';
import { DeploymentRoutingModule } from './deployment-routing.module';
import { DeploymentComponent } from './page/page.component';
import { CardModule } from 'primeng/card';
import { FormsModule } from '@angular/forms';
import { FileUploadModule } from 'primeng/fileupload';
import { ButtonModule } from 'primeng/button';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import {MatInputModule} from '@angular/material/input';
import { ChipsModule } from 'primeng/chips';
import { DividerModule } from 'primeng/divider';
@NgModule({
  declarations: [DeploymentComponent],
  imports: [
    CommonModule,
    DeploymentRoutingModule,
    CardModule,
    ButtonModule,
    FormsModule,
    FileUploadModule,
    MatSnackBarModule,
    MatInputModule,
    ChipsModule,
    DividerModule,
    NgxPermissionsModule.forChild()
  ],
})
export class DeploymentModule {

}
