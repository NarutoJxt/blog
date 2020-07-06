from django.contrib.auth import models
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from account.models import BlogUser


class EmailCheckBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = BlogUser.objects.get(Q(email=username)|Q(username=username))
        except Exception  as e:
            return None
        else:
            if user.check_password(raw_password=password):
                return user