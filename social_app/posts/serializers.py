from .models import *
from rest_framework import serializers
from django.urls import reverse
from django.http import HttpRequest
from django.utils.timezone import now
from django.contrib.auth import get_user_model


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

    post_like = serializers.HyperlinkedIdentityField(
        many=False,
        read_only=True,
        view_name="like-toggle",
        lookup_url_kwarg="post_id",
    )

    post_dislike = serializers.HyperlinkedIdentityField(
        many=False,
        read_only=True,
        view_name="dislike-toggle",
        lookup_url_kwarg="post_id",
    )

    id = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name="post-detail", lookup_url_kwarg="post_id"
    )

    def to_representation(self, instance):
        ret = super(PostSerializer, self).to_representation(instance)
        fields_to_pop = ["post_edit"]
        if instance.creator != self.context["request"].user:
            [ret.pop(field, "") for field in fields_to_pop]
        return ret


class AnalyticsPostSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "count_like",
            "count_dislike",
            "creator",
            "created",
            "likes",
            "dislikes",
            "days_since_created",
        ]

    count_like = serializers.IntegerField()
    count_dislike = serializers.IntegerField()
    days_since_created = serializers.SerializerMethodField()

    def get_days_since_created(self, obj):
        return (now() - obj.created).days


class UsersSerializer(serializers.ModelSerializer):

    last_activity = serializers.DateTimeField()

    class Meta:
        model = get_user_model()
        fields = ("username", "last_login", "last_activity")


class UserPostsSerializer(UsersSerializer):

    post_set = PostSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "last_login", "last_activity", "post_set")
