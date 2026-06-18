import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  form: any = {
    message: '',
    data: {}
  }

  constructor(private router: Router) {

  }

  signIn() {
    if (this.form.data.loginId == 'admin' && this.form.data.password == 'admin') {
      this.form.message = ''
      console.log(this.form.data.loginId, ' ', this.form.data.password)
      localStorage.setItem('name', 'Admin')
      this.router.navigateByUrl('welcome')
    } else {
      this.form.message = 'Login ID & Password Invalid'
    }
  }

  signUp() {
    this.router.navigateByUrl('signup')
  }
}
