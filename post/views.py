from rest_framework import viewsets

from post.models import Comment, CommentVote, Post, PostVote
from post.serializers import (
    CommentSerializer,
    CommentVoteSerializer,
    PostListSerializer,
    PostSerializer,
    PostVoteSerializer,
)
from post.tasks import (
    delete_comment_from_elastic,
    delete_post_from_elastic,
    sync_comment_to_elastic,
    sync_post_to_elastic,
)
from socialnetwork.utils.filters import CommentFilter, PostFilter


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == 200:
            sync_post_to_elastic.delay(response.data["id"])
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            sync_post_to_elastic.delay(response.data["id"])
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            delete_post_from_elastic.delay(kwargs["pk"])
        return response


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    serializer_class = CommentSerializer
    filterset_class = CommentFilter

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == 200:
            sync_comment_to_elastic.delay(response.data["id"])
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            sync_comment_to_elastic.delay(response.data["id"])
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.status_code == 204:
            delete_comment_from_elastic.delay(kwargs["pk"])
        return response


class PostVoteViewSet(viewsets.ModelViewSet):
    queryset = PostVote.objects.all()
    serializer_class = PostVoteSerializer


class CommentVoteViewSet(viewsets.ModelViewSet):
    queryset = CommentVote.objects.all()
    serializer_class = CommentVoteSerializer
