import { Component } from '@angular/core';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {

  message = ''
  firstName = ''
  lastName = ''
  loginId = ''
  password = ''
  dob = ''
  address = ''

  form1 = {
    message: '',
    firstName: '',
    lastName: '',
    loginId: '',
    password: '',
    dob: '',
    address: ''
  }

  form2 = {
    message: '',
    data: {
      firstName: '',
      lastName: '',
      loginId: '',
      password: '',
      dob: '',
      address: ''
    }
  }

  form: any = {
    message: '',
    data: {}
  }

  signUp() {
    console.log(this.form.data)
  }

}