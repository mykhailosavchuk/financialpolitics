export class Post {
    postId: string;
    title: string;
    content: string;
    author: string;
    createdDate: any;
    tags: any;
    img_url: string;


    constructor() {
        this.title = '';
        this.content = '';
        this.img_url = ''
        this.tags = ''
    }
}
