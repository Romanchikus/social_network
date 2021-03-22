from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from posts.views import *
from .yasg import urlpatterns as doc_urls


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "posts": reverse("posts-list", request=request, format=format),
        }
    )


urlpatterns = [
    path("api/", api_root),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("api/", include("posts.urls")),
    path("admin/", admin.site.urls),
]


urlpatterns += doc_urls
