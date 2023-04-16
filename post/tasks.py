from post.models import Comment, Post
from socialnetwork.celery import app
from socialnetwork.utils.elastic import create_update_document, delete_document


@app.task(name="sync.post.to.elastic")
def sync_post_to_elastic(post_id):
    post = Post.objects.get(id=post_id)
    document = {
        "_index": "posts",
        "_id": post.id,
        "_source": {
            "title": post.title,
            "content": post.content,
            "author": post.created_by.username,
            "votes": post.get_post_votes(),
        },
    }
    create_update_document(document, "posts")


@app.task(name="delete.post.from.elastic")
def delete_post_from_elastic(post_id):
    delete_document(post_id, "posts")


@app.task(name="sync.comment.to.elastic")
def sync_comment_to_elastic(comment_id):
    comment = Comment.objects.get(id=comment_id)
    document = {
        "_index": "comments",
        "_id": comment.id,
        "_source": {
            "content": comment.content,
            "author": comment.created_by.username,
            "votes": comment.get_comment_votes(),
        },
    }
    create_update_document(document, "comments")


@app.task(name="delete.comment.from.elastic")
def delete_comment_from_elastic(comment_id):
    delete_document(comment_id, "comments")
