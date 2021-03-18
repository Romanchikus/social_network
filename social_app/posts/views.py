from .models import *
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import *
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from .permissions import IsCreator
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404


class UserDetails(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserPostsSerializer(user, context={"request": request})
        return Response(serializer.data)


class PostCreateViewSet(CreateAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        req = serializer.context["request"]
        serializer.save(creator=req.user)


class PostViewSet(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        posts = Post.objects.all().order_by("-likes")
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return Response(serializer.data)


class PostDetails(APIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_id, format=None):
        post = self.get_object(post_id)
        serializer = PostSerializer(post, context={"request": request})
        return Response(serializer.data)


class PostManaging(PostDetails):

    permission_classes = [permissions.IsAuthenticated, IsCreator]

    def put(self, request, post_id, format=None):

        post = self.get_object(post_id)
        serializer = PostSerializer(
            post, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None):
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes((permissions.IsAuthenticated,))
def likePost(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(owner=user, post=post)

    if not created:  # if exist Like.object
        if like.value == True:
            like.delete()
            post.likes -= 1
            post.save()
            return Response({"response": "deleted"})

        else:  # if Like.object disliked
            post.dislikes -= 1

    like.value = True
    like.save()
    post.likes += 1
    post.save()
    return Response({"response": "liked"})


@api_view(["POST"])
@permission_classes((permissions.IsAuthenticated,))
def dislikePost(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    dislike, created = Like.objects.get_or_create(owner=user, post=post)

    if not created:
        if dislike.value == False:
            dislike.delete()
            post.dislikes -= 1
            post.save()
            return Response({"response": "deleted"})
        else:
            post.likes -= 1

    dislike.value = False
    dislike.save()
    post.dislikes += 1
    post.save()
    return Response({"response": "disliked"})
