from django.urls import include, path
from .views import (
    PostDetails,
    PostViewSet,
    UserDetails,
    PostManaging,
    PostCreateViewSet,
    likePost,
    dislikePost,
)


urlpatterns = [
    path("posts/", PostViewSet.as_view(), name="posts-list"),
    path("posts/<int:post_id>/manage", PostManaging.as_view(), name="post-edit"),
    path("users/<str:username>/", UserDetails.as_view(), name="user-detail"),
    path("posts/<int:post_id>/", PostDetails.as_view(), name="post-detail"),
    path("posts/create/", PostCreateViewSet.as_view(), name="post-create"),
    path("posts/<int:post_id>/like_toggle/", likePost, name="like-toggle"),
    path("posts/<int:post_id>/dislike_toggle/", dislikePost, name="dislike-toggle"),
]