import { Injectable } from "@angular/core";
import { Post } from "../models/Post";
import { AngularFirestore } from "@angular/fire/compat/firestore";
import { map } from "rxjs/operators";
import { Observable } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class NewsService {
  constructor(private db: AngularFirestore) {}

  createPost(post: Post) {
    const postData = JSON.parse(JSON.stringify(post));
    return this.db.collection("newss").add(postData);
  }

  getAllPosts(): Observable<Post[]> {
    const newss = this.db
      .collection<Post>("newss", (ref) => ref.orderBy("createdDate", "desc"))
      .snapshotChanges()
      .pipe(
        map((actions) => {
          return actions.map((c) => ({
            postId: c.payload.doc["id"],
            ...c.payload.doc.data(),
          }));
        })
      );
    return newss;
  }

  getPostbyId(id: string): Observable<Post> {
    const newsDetails = this.db.doc<Post>("newss/" + id).valueChanges();
    return newsDetails;
  }

  updatePost(postId: string, post: Post) {
    const putData = JSON.parse(JSON.stringify(post));
    return this.db.doc("newss/" + postId).update(putData);
  }

  deletePost(postId: string) {
    return this.db.doc("newss/" + postId).delete();
  }
}
