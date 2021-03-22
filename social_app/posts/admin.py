from django.contrib import admin
from posts.models import Post, Like
from django.contrib.auth import get_user_model

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(get_user_model())
# Register your models here.
