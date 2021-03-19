from django.db import models
from django.conf import settings
from django.utils import timezone


def blog_directory_path(instance, filename):
    return "blog_{0}/{1}".format(instance.blog.id, filename)


class Post(models.Model):

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.FileField(upload_to=blog_directory_path, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    description = models.TextField(max_length=1024, default="")


class Like(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.BooleanField(null=True)
    #  created = models.DateTimeField(default=timezone.now, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "owner",
            "post",
        )
