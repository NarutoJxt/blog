#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class AuthMidware(MiddlewareMixin):
    white_url = [settings.MEDIA_URL+"/","/account/login/","/account/register/","/account/reregister/","/account/re_register/","/admin/"]
    def process_request(self,request):
        if request.path_info in self.white_url or request.is_ajax() or str(request.path_info).startswith("/media/") or str(request.path_info).startswith("/oauth/") or str(request.path_info).startswith("/admin/"):
            return None
        elif  str(request.user) == "AnonymousUser":
            url= reverse("account:login")
            return HttpResponseRedirect(url)
