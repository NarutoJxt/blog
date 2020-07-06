import logging
import re
from random import randint

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_delete, pre_delete
from django.dispatch import receiver
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.core.mail import send_mail
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import Truncator
from django.views import View
from django.views.decorators.cache import never_cache, cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, RedirectView, CreateView, ListView, UpdateView
from notifications.signals import notify

from Blog.signals import refresh_cache_signals_save_user, refresh_cache_signals_save_attention, \
    refresh_cache_signals_delete_attention
from account.form import LoginForm, RegisterForm, ReRegisterForm, PersonInfoForm, BaseInfoForm
from account.models import BlogUser, Attention
import time

logger = logging.getLogger("django")
from blogs.models import Artical
from blogs.views import BaseArticleView

User = get_user_model()

class LoginView(FormView):
    form_class = LoginForm
    template_name = "./account/user_login.html"
    success_url = "/"

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)
        if form.is_valid():
            user = form.get_user()
            auth.login(request=self.request, user=user)
            remember = self.request.POST.get("remember")
            response = HttpResponseRedirect(self.get_success_url())
            if remember == "1":
                username = form.cleaned_data["username"]
                response.set_cookie("username", username, expires=60 * 60 * 24)
            return response
        else:
            return self.render_to_response(
                {"form": form}
            )

    def get(self, request, *args, **kwargs):
        username = ""
        password = ""
        try:
            username = request.COOKIES["username"]
        except KeyError as e:
            logger.error(e)
        form = self.form_class()
        form.fields["username"].initial = username
        return self.render_to_response(
            {"form": form}
        )


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        auth.logout(request=request)
        cache.clear()
        url = reverse("account:login")
        return HttpResponseRedirect(url)


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "./account/user_register.html"

    def form_invalid(self, form):
        return self.render_to_response(
            {"form": form}
        )

    def form_valid(self, form):
        flag = 0
        try:
            user = form.save(False)
            send_mail(
                subject="注册事件",
                message="恭喜您已成功注册",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[form.cleaned_data["email"]]
            )
        except Exception as e:
            form.error_messages["email"] = "邮箱不正确，请红心输入"
            flag = 1
        else:
            file_name = self.request.POST.get("username") + self.request.POST["email"] + ".jpg"
            f = self.request.FILES["head_image"]
            content = ContentFile(f.read())
            user.head_path.save(name=file_name, content=content)
            user.save()
        if flag == 1:
            return self.render_to_response(
                {"form":form}
            )
        else:
            url = reverse("account:login")
            return HttpResponseRedirect(url)
    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ReRegisterView(FormView):
    form_class = ReRegisterForm
    template_name = "./account/user_find_password.html"

    def get(self, request, *args, **kwargs):
        form = ReRegisterForm()
        return self.render_to_response(
            {
                "form": form,
            }
        )
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            username = self.request.POST.get("username")
            user = BlogUser.objects.get(username=username)
            password1 = self.request.POST.get("password1")
            user.set_password(password1)
            user.save()
            subject = "修改密码成功"
            msg = "您的密码已修改成功，请妥善保管您的密码"
            email = user.email
            check_email(msg=msg, object=subject, user=email)
            try:
                root = BlogUser.objects.get(username="root")
                notify.send(
                    root,
                    recipient=user,
                    verb='修改了密码',
                    target=user,
                    action_object=user,
                    description="other"
                )
            except Exception as e:
                logger.error(e)
            url = reverse("account:login")
            return JsonResponse(
                {"url":url}
            )




def deal_attention(request):
    if request.is_ajax():
        user = request.user
        status = request.GET.get("status")
        recipient = None
        verb = ""
        target = None
        action_object = None
        if status:
            status = int(status)
            username = request.GET.get("username")
            follower = BlogUser.objects.get(username=username)
            result = ""
            recipient = follower
            if status == 1:
                attention = Attention()
                attention.user = user
                attention.B_follower = follower
                pre_save.connect(refresh_cache_signals_save_attention, sender=Attention)
                data = attention.save()

                result = "您已关注" + username
                verb = "关注了"
                action_object = attention
            elif status == 3:
                try:
                    attention = Attention.objects.get(user=user, B_follower=follower)
                    action_object = attention
                    attention.delete()
                except Exception as e:
                    print(e)
                pre_delete.connect(refresh_cache_signals_delete_attention, sender=Attention)
                result = "您已取消关注" + username
                verb = "取消了关注"


            try:

                notify.send(
                    request.user,
                    recipient=recipient,
                    verb=verb,
                    target=attention,
                    action_object=action_object,
                    description="attention"
                )
            except Exception as e:
                print(e)
            return JsonResponse({
                "result": result
            })
class AttentionView(BaseArticleView):
    template_name = "blogs/attention.html"
    model = Artical
    paginate_by = 8
    key_prefix = "attention_{}_{}"
    def get_follower_list(self):
        follower_list = self.get_cache_data((self.request.user.username,"main_follower_list"))
        follower_list = follower_list   if follower_list else []
        if not follower_list:
            user = BlogUser.objects.get(username=self.request.user.username)
            followers = user.user.all()
            for f in followers:
                follower_list.append(BlogUser.objects.get(username=f.B_follower))
            self.set_cache_data((self.request.user.username, "main_follower_list"), follower_list)
        return follower_list

    def get_queryset(self):
        username = self.request.GET.get("username")
        follower_list = self.get_follower_list()
        article_list = []
        if not username:
            article_list = self.get_cache_data((self.request.user.username, "main_article_list")) \
                if self.get_cache_data((self.request.user.username, "main_article_list")) else []
            if not article_list:
                for f in follower_list:
                    article_list.extend(list(f.article.all()))
                self.set_cache_data((self.request.user.username, "main_article_list"), article_list)
        else:
            user = BlogUser.objects.get(username=username)
            article_list = self.get_cache_data((username, "article_list"))
            article_list = article_list if article_list else []
            if not article_list:
                article_list = Artical.objects.filter(author=user, status="e")
                self.set_cache_data((username, "article_list"), article_list)
        return article_list

    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        user = request.user
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        is_show = True
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data(object_list=self.object_list)

        if self.request.is_ajax():
            try:
                object_list = []
                for o in list(context["object_list"]):
                    temp = {}
                    temp["title"] = o.title
                    img = re.findall(r'img src="(.*?)"', o.body, re.S)
                    if len(img) > 0:
                        img = img[0]
                    else:
                        img = ""
                    temp["img_url"] = img
                    body = re.sub(u"\<.*?\>", "", o.body)
                    body = Truncator(body).chars(70)
                    img_static = settings.DOMAIN + "static/image/design/"
                    thumb_up_img = img_static + "点赞 (5).png"
                    collections_img = img_static + "article_collectio.png"
                    comment_img = img_static + "评论 (3).png"
                    temp["thumb_up_img"] = thumb_up_img
                    temp["collections_img"] = collections_img
                    temp["comment_img"] = comment_img
                    temp["body"] = body
                    temp["comment_counts"] = o.comment_set.count()
                    temp["thump_up_counts"] = o.thumb_up
                    temp["collection_count"] = o.article.count()
                    temp["article_url"] = o.get_absolute_url()
                    object_list.append(temp)
                page_has_next = context["page_obj"].has_next()
                loc = self.request.GET.get("loc")
                return JsonResponse(
                    {
                        "object_list": object_list,
                        "page_has_next": page_has_next,
                        "loc": loc
                    }
                )
            except Exception as e:
                print(e)
        else:

            follower_list = self.get_follower_list()
            collection_count = 0
            character_count = 0
            username = self.request.GET.get("username")
            for article in self.object_list:
                collection_count += article.article.count()
                character_count += len(article.body)
            context["collection_count"] = collection_count
            context["character_count"] = character_count
            context["follower_list"] = follower_list
            if not username:
                context["username"] = ""
                context["type"] = 1
                is_show = False
            else:
                context["username"] = username
                context["author"] = BlogUser.objects.get(username=username)
                context["type"] = 2
                is_show = True
            context["is_show"] = is_show
            return self.render_to_response(context)
class PersonInfoView(UpdateView):
    template_name = "blogs/editarticle/person_info.html"
    form_class = PersonInfoForm
    model = User
    def form_invalid(self, form):
        return self.render_to_response(
            {"form":form}
        )
    def form_valid(self, form):
        import os
        username = form.cleaned_data["username"]
        user = BlogUser.objects.get(username=username)
        if form.cleaned_data["head_path"] != user.head_path:
            img_path = settings.MEDIA_ROOT+"/"+str(user.head_path)
            os.remove(img_path)
        user = form.save()
        user.save()
        return HttpResponseRedirect(user.get_info_url())


#"基础设置试图"

class BaseInfoView(UpdateView):
    template_name = "blogs/editarticle/base_info.html"
    form_class = BaseInfoForm
    model = User

    # @method_decorator(cache_page(60 * 15), name="base_info_get")
    def get(self, request, *args, **kwargs):
        return super(BaseInfoView,self).get(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        return super(BaseInfoView,self).post(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseInfoView,self).get_context_data(**kwargs)
        return context
    def form_invalid(self, form):
        user = form.save()
        user.save()
        return HttpResponseRedirect(reverse("account:get_base_info",kwargs={
            "pk":self.request.user.pk
        }))
#找回密码视图
def modify_password(request):
    get_type = request.GET.get("type")
    if get_type == "show":
        return render(request,"account/modify_pwd.html")
    elif get_type == "modify":
        user = BlogUser.objects.get(username=request.user.username)
        user.set_password(request.POST.get("password"))
        user.save()
        url = reverse(
            "account:login"
        )
        return JsonResponse(
            {"url":url}
        )
    else:
        user = BlogUser.objects.get(username=request.user.username)
        url = user.get_info_url()
        return JsonResponse(
            {"url":url}
        )


@csrf_exempt
def getImg(request):
    # if request.is_ajax():
    body = request.POST.get("showImg")
    try:
        user = BlogUser.objects.get(username=body)
    except Exception as e:
        url = reverse("account:register")
        return HttpResponseRedirect(url)
    else:
        img_path = settings.MEDIA_URL + "/" + str(user.head_path)
        return JsonResponse({"a": img_path})


def check_email(msg, object, user):
    send_mail(
        subject=object,
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user]
    )
@csrf_exempt
def edit_signature(request):
    signature = request.POST.get("signature")
    user = request.user
    user.signature = signature
    user.save()
    url = reverse("blog:person")
    return redirect(url)
def get_cache_data(key,expire=10*60):
    code = cache.get(key)
    is_expire = False
    if not code:
        code = ""
        for i in range(4):
            code += str(randint(0, 9))
        cache.set(key, code,0, expire)
        return code,is_expire
    else:
        is_expire = True
        return code,is_expire
def get_code(request):

    email = request.POST.get("email")
    get_type = request.POST.get("type")
    if get_type == "find":
        try:
            user = BlogUser.objects.get(email=email)
        except Exception as e:
            error = "邮箱对应的用户不存在"
            return JsonResponse(
                data={
                    "res":0,
                   "error":error
                }
            )
        else:
            code,is_expire = get_cache_data(email+"_code")
            msg = ""
            if not is_expire:
                check_email(code, "邮箱验证", email)
                msg = "验证码已发送"
            else:
                msg = "验证码未过期"
            return JsonResponse(
                data={
                    "code": code,
                    "username":user.username,
                    "res":1,
                    "msg":msg
                }
            )

    else:
        if not email:
            email = request.user.email
        code,is_expire = get_cache_data(email+"_code",10*60)
        msg = ""
        if not is_expire:
            check_email(code, "邮箱验证", email)
            msg = "验证码已发送"
        else:
            msg = "验证码未过期"
        return JsonResponse(
            data={
                "code": code,
                "email":email,
                "msg":msg
            }
        )
def update_email(request):
    user = BlogUser.objects.get(username=request.user.username)
    email = request.GET.get("email")
    user.email = email
    error = ""
    url = ""
    try:
        user.save()
    except Exception as e:
        error = "邮箱已存在，请重新输入"
    else:
        url = user.get_info_url()
    return JsonResponse(
        {
            "url":url,
            "error":error
         }
    )