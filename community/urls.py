from django.urls import path

from community.views import CommunityViewSet

urlpatterns = [
    path("", CommunityViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "<uuid:pk>/",
        CommunityViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
]
