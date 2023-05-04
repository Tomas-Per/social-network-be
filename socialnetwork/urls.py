from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("api/communities/", include("community.urls")),
    path("api/posts/", include("post.urls")),
]
