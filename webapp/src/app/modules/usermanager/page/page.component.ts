import {Component, OnInit} from '@angular/core';
import {UsermanagmentApiService} from "../../../services/usermanagment-api.service";
import {MessageService} from "primeng/api";
import {FormBuilder, FormControl, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-page',
  templateUrl: './page.component.html',
  styleUrls: ['./page.component.scss'],
  providers: [MessageService]
})

export class PageComponent implements OnInit{
  myGroup!: FormGroup
  constructor(
    private service:UsermanagmentApiService,
    private messageService:MessageService,
    private fb: FormBuilder
  ) { }

  users! : any[]
  username!: string;
  firstname!: string;
  lastname!:string;
  email!: string;
  password!: string;
  productDialog: boolean = false;
  groups!: any[];
  checked: boolean = false;
  selectedValue: any;
  editingUser!: string;
  async ngOnInit(): Promise<void> {
    this.users = await this.getUsers()

  }


  async getUsers(): Promise<any>{
    this.service.getUsers().subscribe((data: any) => {this.users = data})
  }

  async deleteUser(userid:string){
    this.service.removeUser(userid).subscribe({
      next:(v) => {
        this.messageService.add({severity:'success', summary:'Success', detail:'User Deleted'})
        this.testA()
      },
      error:(e) => {this.messageService.add({severity:'error', summary:'Error', detail:e["error"]["message"]["errorMessage"]})},
      complete: () => console.info("complete")
      }
    )
  }
  async createUser(){
    this.service.createUser(
      this.username,
      this.firstname,
      this.lastname,
      this.email,
      this.password).subscribe(
      {
        next: (v) => {
          this.users.push(v)
          this.messageService.add({severity:'success', summary:'Success', detail:'User Created'})
        },
        error: (e) => {
          this.messageService.add({severity:'error', summary:'Error', detail:e["error"]["message"]["errorMessage"]})
        },
        complete: () => console.info('complete')
      }
    )
  }

  async testA(){
    this.service.getUsers().subscribe((data: any) => {this.users = data})
  }

  async editUser(user: any) {
    this.productDialog = true
    this.editingUser = user
    this.service.getUserRoles(user).subscribe(
      {
        next: (v:any) => {
          if (v.length > 0){
            this.selectedValue = v[0].name
          }
        },
        error: (e) => {
          this.messageService.add({severity:'error', summary:'Error', detail:e["error"]["message"]["errorMessage"]})
        },
        complete: () => console.info('complete')
      }
    )

    this.service.getAllGroups().subscribe(
      {
        next: (v:any) => {
          this.groups = v
        },
        error: (e) => {
          this.messageService.add({severity:'error', summary:'Error', detail:e["error"]["message"]["errorMessage"]})
        },
        complete: () => console.info('complete')
      }
    )
  }



  changeValue() {
    this.service.setUserGroup(this.editingUser,this.selectedValue).subscribe(
      {
        next: (v:any) => {},
        error: (e) => {
          this.messageService.add({severity:'error', summary:'Error', detail:e["error"]["message"]["errorMessage"]})
        },
        complete: () => {
          this.productDialog = false
          this.selectedValue = ""
        }
      }
    )
  }


}
