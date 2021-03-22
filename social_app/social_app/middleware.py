from datetime import timedelta as td
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model


class LastUserActivityMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get(self.KEY)

            # If key is old enough, update database.
            too_old_time = timezone.now() - td(
                seconds=settings.LAST_ACTIVITY_INTERVAL_SECS
            )
            if not last_activity or last_activity < too_old_time:
                user = get_user_model().objects.get(pk=request.user.pk)
                user.last_activity = timezone.now().isoformat()
                user.save()
            request.session[self.KEY] = timezone.now()
        response = self.get_response(request)
        return response

    KEY = "last-activity"

    def process_request(self, request):

        return None


from rest_framework_simplejwt.authentication import JWTAuthentication


class LastUserActivityJWT(JWTAuthentication):
    def get_user(self, validated_token):

        user = super().get_user(validated_token)
        too_old_time = timezone.now() - td(seconds=settings.LAST_ACTIVITY_INTERVAL_SECS)
        if not user.last_activity or user.last_activity < too_old_time:
            user.last_activity = timezone.now().isoformat()
            user.save()

        return user
