import { Component, OnInit } from '@angular/core';
import { AuthService } from './services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  constructor(
    private authService: AuthService,
    private router: Router) { }

ngOnInit() {
    this.authService.appUser$.subscribe(user => {
      if (!user) {
        return;
      } else {
        /*
         * If the user is logged in fetch the return URL from local storage.
         * Navigate to the return URL if available.
         */
        const returnUrl = localStorage.getItem('returnUrl');
        if (!returnUrl) {
          return;
        }
        localStorage.removeItem('returnUrl');
        this.router.navigateByUrl(returnUrl);
      }
    });
  }

  ngAfterViewInit() {
    try {
      (window['adsbygoogle'] = window['adsbygoogle'] || []).push({});

      // If you have two ad on the page, then add this again.
      //(window['adsbygoogle'] = window['adsbygoogle'] || []).push({});


    } catch (e) {}
   }
}


