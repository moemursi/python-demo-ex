import { Component } from '@angular/core';

import {
  IonicPage,
  NavController,
  NavParams,
  AlertController
} from 'ionic-angular';

import { AuthServiceProvider } from '../../providers/auth-service/auth-service';

/**
 * Generated class for the LoginPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage {

  formData = { email: "", password: "" };
  errorMsg: string;

  constructor(
    public navCtrl: NavController,
    public navParams: NavParams,
    public authService: AuthServiceProvider,
    private alertCtrl: AlertController) {}

  ionViewDidEnter() {
    console.log('ionViewDidEnter LoginPage');
  }

  async login() {
    try {
      const authResponse = await this.authService.doAuth(this.formData);

      // Auth successfull. Remember token in local storage.
      console.log("Auth API successfull, token=" + authResponse.token);
      localStorage.setItem('authToken', JSON.stringify(authResponse.token));

      // Erase all previous navigation history and make HomePage the root
      this.navCtrl.setRoot('RegisterSalonPage');
    }
    catch (e) {
      // Error log
      console.log("Login failed:" + JSON.stringify(e));

      // Show an error message
      const alert = this.alertCtrl.create({
        title: 'Login failed',
        subTitle: 'Invalid email or password',
        buttons: ['Dismiss']
      });
      alert.present();
    }
  }
}
