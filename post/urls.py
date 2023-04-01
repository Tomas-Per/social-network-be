from django.urls import path

from post.views import CommentViewSet, CommentVoteViewSet, PostViewSet, PostVoteViewSet

urlpatterns = [
    path("", PostViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "<uuid:pk>/",
        PostViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
    ),
    path("comments/", CommentViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "comments/<uuid:pk>/",
        CommentViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
    ),
    path("votes/", PostVoteViewSet.as_view({"get": "list", "post": "create"})),
    path("votes/<uuid:pk>/", PostVoteViewSet.as_view({"get": "retrieve", "delete": "destroy"})),
    path("comment-votes/", CommentVoteViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "comment-votes/<uuid:pk>/",
        CommentVoteViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
    ),
]
