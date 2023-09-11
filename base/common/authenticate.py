import logging
import os

import jwt
from django.apps import apps
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from user.models import User

logger = logging.getLogger(__name__)


class Token(BaseAuthentication):
    def authenticate(self, request):

        access_token = request.META.get("HTTP_TOKEN", None)

        if not access_token or access_token == "undefined":
            return None
        try:
            decoded = jwt.decode(access_token, key=os.environ["SECRET_KEY"], algorithm="HS256")
        except Exception as ex:
            print(ex)
            return None

        user = apps.get_model("user", "User")
        user_index = decoded.get("user_index")

        try:
            user = user.objects.get(user_index=user_index)
            return user
        except user.DoesNotExist:
            raise exceptions.AuthenticationFailed({"success": 0, "results": "authentication failed"})