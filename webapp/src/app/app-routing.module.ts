import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {AppLayoutComponent} from "./shared/layout/app.layout.component";
import {AuthGuard} from "./shared/guards/auth.guard";
import { NgxPermissionsGuard } from 'ngx-permissions';

const routes: Routes = [
  {
    path: '',
    component: AppLayoutComponent,
    canActivate: [AuthGuard],
    data: {
      roles: ['admin'],
    },
    children: [
      {
        path: '',
        canActivate: [AuthGuard],
        loadChildren: () =>
          import(
            './modules/home/home.module'
            ).then((m) => m.HomeModule),
        data:{
          permissions: {
            only: "admin"
          }
        }

      },
      {
        path: 'datamanager',
        canActivate: [AuthGuard,NgxPermissionsGuard],
        loadChildren: () =>
          import(
            './modules/datamanager/datamanager.module'
            ).then((m) => m.DatamanagerModule),
            data:{
              permissions: {
                only: "admin"
              }

            }
      },
      {
        path: 'usermanager',
        canActivate: [AuthGuard,NgxPermissionsGuard],
        loadChildren: () =>
          import(
            './modules/usermanager/usermanager.module'
            ).then((m) => m.UsermanagerModule),
        data:{
          permissions: {
            only: "admin"
          }
        }
      },
      {
        path: 'deployment',
        canActivate: [AuthGuard,NgxPermissionsGuard],
        loadChildren: () =>
        import(
          './modules/deployment/deployment.module'
          ).then((m) => m.DeploymentModule),
        data:{
          permissions: {
            only: "admin"
          }
        }
      }
    ],
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
        useHash: true,
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {
}
