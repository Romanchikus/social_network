from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from posts.views import *
from users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "posts": reverse("posts-list", request=request, format=format),
        }
    )


urlpatterns = [
    path("", api_root),
    path("auth/", include("djoser.urls")),
    path("api/", include("posts.urls")),
    path("admin/", admin.site.urls),
]
