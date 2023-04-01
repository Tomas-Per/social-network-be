from rest_framework import viewsets

from post.models import Comment, CommentVote, Post, PostVote
from post.serializers import (
    CommentSerializer,
    CommentVoteSerializer,
    PostSerializer,
    PostVoteSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent_comment__isnull=True)
    serializer_class = CommentSerializer


class PostVoteViewSet(viewsets.ModelViewSet):
    queryset = PostVote.objects.all()
    serializer_class = PostVoteSerializer


class CommentVoteViewSet(viewsets.ModelViewSet):
    queryset = CommentVote.objects.all()
    serializer_class = CommentVoteSerializer
