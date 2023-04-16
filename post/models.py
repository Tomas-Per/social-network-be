from django.conf import settings
from django.db import models

from community.models import Community
from socialnetwork.utils.mixins import DefaultUUIDMixin, DefaultValuesMixin


class Post(DefaultUUIDMixin, DefaultValuesMixin):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=280)
    url = models.URLField("URL", max_length=200, null=True, blank=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts")

    def get_post_votes(self):
        return (
            self.post_votes.filter(vote_type=1).count()
            - self.post_votes.filter(vote_type=-1).count()
        )

    def __str__(self) -> str:
        return self.title


class Comment(DefaultUUIDMixin, DefaultValuesMixin):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    content = models.CharField(max_length=280)

    def get_comment_votes(self):
        return (
            self.comment_votes.filter(vote_type=1).count()
            - self.comment_votes.filter(vote_type=-1).count()
        )

    def __str__(self) -> str:
        return self.content


class CommentVote(DefaultUUIDMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment_votes")
    vote_type = models.IntegerField(choices=((1, "Upvote"), (-1, "Downvote")))

    class Meta:
        unique_together = ("user", "comment")
        verbose_name_plural = "Comment votes"
        verbose_name = "Comment vote"

    def __str__(self) -> str:
        return f"{self.user} voted {self.vote_type} on {self.comment.id}"


class PostVote(DefaultUUIDMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_votes")
    vote_type = models.IntegerField(choices=((1, "Upvote"), (-1, "Downvote")))

    class Meta:
        unique_together = ("user", "post")
        verbose_name_plural = "Post votes"
        verbose_name = "Post vote"

    def __str__(self) -> str:
        return f"{self.user} voted {self.vote_type} on {self.post.title}"
