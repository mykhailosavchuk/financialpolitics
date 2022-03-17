import { BrowserModule } from "@angular/platform-browser";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgModule } from "@angular/core";
import { AppComponent } from "./app.component";
import { environment } from "../environments/environment";
import { RouterModule } from "@angular/router";
import { CKEditorModule } from "@ckeditor/ckeditor5-angular";
import { FormsModule } from "@angular/forms";
import { HttpClientModule } from "@angular/common/http";
import { NgMaterialModule } from "./ng-material/ng-material.module";
import { NgxPaginationModule } from "ngx-pagination";
import { NewsComponent } from "./components/news/news.component";
import { CommentsComponent } from "./components/comments/comments.component";
import { HomeComponent } from "./components/home/home.component";
import { NavBarComponent } from "./components/nav-bar/nav-bar.component";
import { ScrollerComponent } from "./components/scroller/scroller.component";
import { NewsEditorComponent } from "./components/news-editor/news-editor.component";
import { NewsCardComponent } from "./components/news-card/news-card.component";
import { ExcerptPipe } from "./customPipes/excerpt.pipe";
import { SlugPipe } from "./customPipes/slug.pipe";
import { SocialShareComponent } from "./components/social-share/social-share.component";
import { PaginatorComponent } from "./components/paginator/paginator.component";
import { AuthorProfileComponent } from "./components/author-profile/author-profile.component";
import { AuthGuard } from "./guards/auth.guard";
import { AdminAuthGuard } from "./guards/admin-auth.guard";
import { ShareIconsModule } from "ngx-sharebuttons/icons";
import { ShareButtonsConfig, ShareModule } from "ngx-sharebuttons";
import { FontAwesomeModule } from "@fortawesome/angular-fontawesome";
import { AngularFirestoreModule } from "@angular/fire/compat/firestore";
import { AngularFireModule } from "@angular/fire/compat";
import { AboutusComponent } from "./components/aboutus/aboutus.component";

const customConfig: ShareButtonsConfig = {
  autoSetMeta: true,
  twitterAccount: "HiTechDemocracy",
};

@NgModule({
  declarations: [
    AppComponent,
    NewsComponent,
    CommentsComponent,
    HomeComponent,
    NavBarComponent,
    ScrollerComponent,
    NewsEditorComponent,
    NewsCardComponent,
    ExcerptPipe,
    SlugPipe,
    SocialShareComponent,
    PaginatorComponent,
    AuthorProfileComponent,
  ],
  imports: [
    AngularFireModule.initializeApp(environment.firebaseConfig),
    AngularFirestoreModule,
    ShareIconsModule,
    NgxPaginationModule,
    HttpClientModule,
    FontAwesomeModule,
    ShareModule.withConfig(customConfig),
    BrowserModule,
    BrowserAnimationsModule,
    NgMaterialModule,
    CKEditorModule,
    FormsModule,
    RouterModule.forRoot(
      [
        { path: "", component: HomeComponent, pathMatch: "full" },
        { path: "page/:pagenum", component: HomeComponent },
        { path: "aboutus", component: AboutusComponent },

        {
          path: "addpost",
          component: NewsEditorComponent,
          canActivate: [AuthGuard],
        },
        {
          path: "editpost/:id",
          component: NewsEditorComponent,
          canActivate: [AdminAuthGuard],
        },
        { path: "news/:id/:slug", component: NewsComponent },
        { path: "**", component: HomeComponent },
      ],
      { relativeLinkResolution: "legacy" }
    ),
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
