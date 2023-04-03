from django.contrib import admin

from post.models import Comment, CommentVote, Post, PostVote
from socialnetwork.utils.mixins import BaseAdminMixin


@admin.register(Post)
class PostAdmin(BaseAdminMixin):
    list_display = ("id", "community", "title")


@admin.register(Comment)
class CommentAdmin(BaseAdminMixin):
    list_display = ("id", "post", "parent_comment", "content", "created_at", "created_by")


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    pass
