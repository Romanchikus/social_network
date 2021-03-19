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
            "api/token/": reverse("token_obtain_pair", request=request, format=format),
            "api/token/refresh/": reverse(
                "token_refresh", request=request, format=format
            ),
        }
    )


router = routers.DefaultRouter()
router.register(r"api/users", UserViewSet)

urlpatterns = [
    path("", api_root),
    # path('', include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include("posts.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]
