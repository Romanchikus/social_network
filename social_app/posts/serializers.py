from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    creator = serializers.HyperlinkedRelatedField(
        view_name="user-detail",
        source="creator.username",
        read_only=True,
        lookup_url_kwarg="username",
    )

    post_edit = serializers.HyperlinkedIdentityField(
        many=False,
        read_only=True,
        view_name="post-edit",
        lookup_url_kwarg="post_id",
    )

    # post_like = serializers.HyperlinkedIdentityField(
    #     many=False,
    #     view_name="post-like",
    #     lookup_url_kwarg="post_id",
    # )

    id = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="post-detail", lookup_url_kwarg="post_id"
    )

    # likes = serializers.ReadOnlyField()
    # dislikes = serializers.ReadOnlyField()

    def to_representation(self, instance):
        ret = super(PostSerializer, self).to_representation(instance)
        fields_to_pop = ["post_edit"]
        if instance.creator != self.context["request"].user:
            [ret.pop(field, "") for field in fields_to_pop]
        return ret


class UserPostsSerializer(serializers.ModelSerializer):

    post_set = PostSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "post_set")
