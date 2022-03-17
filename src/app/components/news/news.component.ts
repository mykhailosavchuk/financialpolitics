import { Component, OnDestroy, ViewEncapsulation } from "@angular/core";
import { Post } from "src/app/models/post";
import { ActivatedRoute, ParamMap } from "@angular/router";
import { NewsService } from "src/app/services/news.service";
import { Observable, Subject } from "rxjs";
import { takeUntil } from "rxjs/operators";

@Component({
  selector: "app-news",
  templateUrl: "./news.component.html",
  styleUrls: ["./news.component.scss"],
  encapsulation: ViewEncapsulation.None,

})
export class NewsComponent implements OnDestroy {
  postData$: Observable<Post>;
  postId;
  private unsubscribe$ = new Subject<void>();

  constructor(private route: ActivatedRoute, private newsService: NewsService) {
    this.route.paramMap
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe((params: ParamMap) => {
        this.postId = params.get("id");
        this.postData$ = this.newsService.getPostbyId(this.postId);
      });
  }

  ngOnDestroy() {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }
}
