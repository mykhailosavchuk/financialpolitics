import { Component, OnInit, OnDestroy } from "@angular/core";
import { NewsService } from "src/app/services/news.service";
import { Post } from "src/app/models/post";
import { ActivatedRoute, ParamMap } from "@angular/router";
import { AuthService } from "src/app/services/auth.service";
import { CommentService } from "src/app/services/comment.service";
import { SnackbarService } from "src/app/services/snackbar.service";
import { Observable, Subject } from "rxjs";
import { takeUntil } from "rxjs/operators";

@Component({
  selector: "app-news-card",
  templateUrl: "./news-card.component.html",
  styleUrls: ["./news-card.component.scss"],
})
export class NewsCardComponent implements OnInit, OnDestroy {
  config: any;
  pageSizeOptions = [];
  newsPost$: Observable<Post[]>;
  appUser$ = this.authService.appUser$;
  private unsubscribe$ = new Subject<void>();

  constructor(
    private newsService: NewsService,
    private commentService: CommentService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private snackBarService: SnackbarService
  ) {
    this.pageSizeOptions = [3, 6, 9];
    const pageSize = sessionStorage.getItem("pageSize");
    this.config = {
      currentPage: 1,
      itemsPerPage: pageSize ? +pageSize : this.pageSizeOptions[0],
    };
  }

  ngOnInit() {
    this.route.paramMap
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((params: ParamMap) => {
        this.config.currentPage = params.get("pagenum");
        this.newsPost$ = this.newsService.getAllPosts();
      });
  }

  delete(postId: string) {
    if (confirm("Are you sure?")) {
      this.newsService.deletePost(postId).then(() => {
        this.commentService.deleteAllCommentForNews(postId);
        this.snackBarService.showSnackBar("News post deleted successfully");
      });
    }
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
