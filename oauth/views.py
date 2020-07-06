import urllib
from datetime import datetime
from random import random, randint
from urllib.request import urlretrieve

from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import FormView
from notifications.signals import notify

from account.models import BlogUser
from oauth.OauthManager import BaseOauthManager
from oauth.forms import EmailCheckForm
from oauth.models import OauthConfig, OauthUser

class EmailCheckRequiredView(FormView):
    form_class = EmailCheckForm
    template_name = "account/email_bind.html"
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        flag = 0
        try:
            send_mail(
                subject="绑定时间",
                message="恭喜您已经绑定您的邮箱到本平台，正在进行邮箱验证，接下来会给您发送您的注册信息，请妥善保管",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data["email"]]
            )
        except Exception as e:
            form.error_messages["email"] = "邮箱不可用，请重新输入"
            flag = 1
        else:
            oauthid = self.request.POST.get("oauthid")
            user = OauthUser.objects.get(pk=oauthid)
            try:
                temp = OauthUser.objects.get(email=email, user_type=user.user_type)
            except ObjectDoesNotExist as e:
                user.email = email
            else:
                user = temp
                login(self.request, user.user)
                return HttpResponseRedirect(reverse("blog:index"))
            message = ""
            try:
                author = get_user_model().objects.get(email=email)
            except ObjectDoesNotExist as e:
                author = BlogUser()
                author.username = "DjangoBlog_"+"".join([str(randint(0,9)) for i in range(4)])
                password = author.username
                author.set_password(password)
                head_path = settings.MEDIA_ROOT + "/static/image/head/" + user.nickname + user.openid + user.picture[-3:]
                urlretrieve(user.picture, head_path)
                head_path = "/static/image/head/" + user.nickname + user.openid + user.picture[-3:]
                author.head_path = head_path
                author.email = email
                message = "您的用户名为:"+author.username+"初始密码为："+password+"，请妥善保管您的密码,并及时登录平台修改您的密码"
            else:
                message = "您已成功登录本平台，并绑定了第三方平台"
            user.user = author
            if user.user_type == "github":
                author.user_type = "1"
            elif user.user_type == "geogle":
                author.user_type = "2"
            author.save()
            user.save()
            send_mail(
                subject="绑定时间",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data["email"]],
            )
            root = BlogUser.objects.filter(is_superuser=True)[0]
            notify.send(
                root,
                recipient=author,
                verb='使用第三方平台登录',
                target=author,
                action_object=user,
                description="other"
            )
            login(self.request,author)

        if flag == 1:
            return self.render_to_response(
                {"form":form}
            )
        else:
            return HttpResponseRedirect(reverse("blog:index"))
def get_app():
    configs = OauthConfig.objects.filter(is_enable=True).all()
    if not configs:
        configs = []
    config_types = [c.type for c in configs]
    applications = BaseOauthManager.__subclasses__()

    apps = [a() for a in applications if a().ICON_NAME.lower() in config_types]
    return apps


def get_manager_by_type(type):
    apps = get_app()
    if apps:
        finds = list(filter(lambda x:x.ICON_NAME.lower()==type.lower(),apps))
        if finds[0]:
            return finds[0]
def authorize(request):
    type = request.GET.get("type")
    if not type:
        return HttpResponseRedirect(reverse("account:login"))
    manager = get_manager_by_type(type)
    if not manager:
        return HttpResponseRedirect(reverse("account:login"))
    code = request.GET.get("code",None)
    access_token = manager.get_access_token_by_code(code)

    if not access_token:
        return HttpResponseRedirect(manager.get_authorize_url())
    user,is_exist = manager.get_auth_info()
    if not is_exist:
        if user:
            if not user.nickname:
                user.nickname = "djangoBlog"+ datetime.now()
            email = user.email
            if email:
                try:
                    temp = OauthUser.objects.get(email=email, user_type=user.user_type)
                except ObjectDoesNotExist as e:
                    user.email = email
                else:
                    user = temp
                    login(request,user.user)
                    return HttpResponseRedirect(reverse("blog:index"))
                message = ""
                try:
                    author = get_user_model().objects.get(email=email)
                except ObjectDoesNotExist as e:
                    author = BlogUser
                    author.username = user.nickname
                    author.password = author.set_password(author.username+user.user_type)
                    head_path = settings.MEDIA_ROOT + "/static/image/head/" + user.nickname + user.openid + user.picture[-3:]
                    urlretrieve(user.picture, head_path)
                    head_path = "/static/image/head/" + user.nickname + user.openid + user.picture[-3:]
                    author.head_path = head_path
                    message = "您的用户名为:" + author.username + "初始密码为：" + author.username + user.user_type + "，请妥善保管您的密码"
                else:
                    message = "您已成功登录本平台，并绑定了第三方平台"
                user.user = author
                if user.user_type == "github":
                    author.user_type = "1"
                elif user.user_type == "geogle":
                    author.user_type = "2"

                author.save()
                user.save()
                send_mail(
                    subject="绑定时间",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                )
                login(request,author)
                return HttpResponseRedirect(reverse("blog:index"))
            else:
                user.save()
                url = reverse("oauth:bindEmail",kwargs={
                    "oauthid":user.id
                })
                return HttpResponseRedirect(url)
    else:
        author = BlogUser.objects.get(email=user.email)
        login(request,author)
        return HttpResponseRedirect(reverse("blog:index"))

def oauth_login(request):
    type = request.GET.get("type",None)
    if not type:
        return HttpResponseRedirect(reverse("account:login"))
    manager = get_manager_by_type(type)
    if not manager:
        return HttpResponseRedirect(reverse("account:login"))

    url = manager.get_authorize_url()
    return HttpResponseRedirect(url)
