from .models import *
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import UserPostsSerializer, PostSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from .permissions import IsCreator
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse


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
        req = serializer.context['request']
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