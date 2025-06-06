import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {HomeComponent} from "./pages/dashboard/home.component";

@NgModule({
  imports: [RouterModule.forChild([
    {
      path: '',
      children: [
        {
          path: '',
          component: HomeComponent
        },
      ],

    }
  ])],
  exports: [RouterModule]
})
export class HomeRoutingModule {
}
