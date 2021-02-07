from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from jiranapp.models import *

import re


class LoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            if re.match(r"[^@]+@[^@]+\.[^@]+", username):
                user = UserModel.objects.get(email=username)
            
            elif username.isdecimal():
                user = UserModel.objects.get(phone=username)
            
            else:
                user = UserModel.objects.get(username=username)

        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None