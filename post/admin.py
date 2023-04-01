from django.contrib import admin

from post.models import Comment, CommentVote, Post, PostVote


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "community", "title")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "parent_comment", "content", "created_at", "created_by")


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):
    pass


@admin.register(CommentVote)
class CommentVoteAdmin(admin.ModelAdmin):
    pass
