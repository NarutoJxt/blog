
import logging
import re
import datetime

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import pre_save, pre_delete

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.text import Truncator
from django.views.decorators.cache import  never_cache
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, RedirectView
from haystack.generic_views import SearchView
from notifications.signals import notify

from Blog.signals import refresh_cache_signals_save_articles, refresh_cache_signals_delete_articles
from account.models import BlogUser, Attention

from blogs.form import ArticleEditForm, MySearchForm
from collection.models import Collection
from comment.form import CommentForm
from blogs.models import Artical
from appeal.forms import AppealForm
import math
logger = logging.getLogger("django")



class BaseArticleView(ListView):
    paginate_by = 5
    key_prefix = ""

    def get_cache_data(self,key):
        key = self.key_prefix.format(key[0],key[1])
        if cache.get(key):
            res = cache.get(key)
            return res
        else:
            return None
    def set_cache_data(self,key,value):
        key = self.key_prefix.format(key[0],key[1])
        cache.set(key,value)

class IndexView(BaseArticleView):
    template_name = "blogs/article_index.html"
    cur_page = 1
    key_prefix = "article-index-{}-{}"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

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
        context = self.get_context_data()

        if request.is_ajax():
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
                    img_static = settings.DOMAIN+"static/image/design/"
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
                        "object_list":object_list,
                        "page_has_next":page_has_next,
                        "loc":loc
                    }
                )
            except Exception as e:
                print(e)
        else:
            headers = self.get_queryset().order_by("-views")[:5]
            context["headers"] =headers
            return self.render_to_response(context)
    def get_queryset(self):
        articles = self.get_cache_data(("article",""))
        if not articles:
            articles = Artical.objects.filter(status="e")
            self.set_cache_data(("articles",""),articles)
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        img_path = settings.MEDIA_URL + "/" + str(self.request.user.head_path)
        context["img_path"] = img_path
        context["user"] = self.request.user
        return context



class Article_Detail(DetailView):
    template_name = "blogs/article_detail.html"
    model = Artical
    context_object_name = "article"
    pk_url_kwarg = "article_id"
    def dispatch(self, request, *args, **kwargs):
        return super(Article_Detail,self).dispatch(request,*args,**kwargs)


    def get_object(self, queryset=None):
        obj = super(Article_Detail, self).get_object(queryset=queryset)
        self.obj = obj
        self.obj.viewed()
        return obj

    def get_context_data(self, **kwargs):
        context = super(Article_Detail, self).get_context_data(**kwargs)
        comment_form = CommentForm()
        comment_form.fields.update({
            "name": forms.CharField(widget=forms.HiddenInput),
            "article_id": forms.IntegerField(widget=forms.HiddenInput),
            "email": forms.EmailField(widget=forms.HiddenInput)
        })

        follower_list = []
        user = BlogUser.objects.get(username=self.request.user.username)
        followers = user.user.all()
        for f in followers:
            follower_list.append(BlogUser.objects.get(username=f.B_follower))
        user = self.request.user
        username = user.username
        comment_form.fields["name"].initial = username
        comment_form.fields["article_id"].initial = self.obj.id
        appeal_form = AppealForm()
        appeal_form.fields["appealed_article"].initial = self.obj
        context["appeal_form"] = appeal_form
        result = Collection.objects.filter(blog_user__username=username,collected_article=self.obj)
        is_collected = False
        if result:
            is_collected = True
        else:
            is_collected = False
        context["follower_list"] = follower_list
        context["is_collected"] = is_collected
        collected_count = Collection.objects.filter(collected_article=self.obj).count()
        context["collected_count"] = collected_count
        comment_form.fields["email"].initial = user.email
        img_path = cache.get("img_path", None)
        if not img_path:
            img_path = settings.MEDIA_URL+"/"+str(user.head_path)
        context["img_path"] = img_path
        context["comment_dict"], context["header"] = self.obj.get_comment_list()
        context["form"] = comment_form
        follower = context["object"].author
        if follower.username != self.request.user.username:
            context["is_show"] = True
            if follower in follower_list:
                context["is_follower"] = True
            else:
                context["is_follower"] = False
        else:
            context["is_show"] = False
        return context

class ArticleDealView(RedirectView):
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                get_type  = request.POST.get("type")
                title = request.POST.get("title")
                username = request.POST.get("author")
                author = BlogUser.objects.get(username=username)
                article = Artical.objects.get(title=title,author=author)
                result = 0
                recipient = author
                verb = ""
                target = article
                action_object = None
                description = ""
                if get_type == "thumb_up":#点赞
                    article.thumb_up+=1
                    article.save()
                    result = 1
                    verb = "点赞"
                    description = "thump"
                    action_object = "thump"
                if get_type == "collection":  # 收藏
                    collection = Collection(blog_user=self.request.user, collected_article=article)
                    collection.save()
                    result = 3
                    verb = "收藏"
                    description = "collection"
                    action_object = collection
                elif get_type == "cancleCollection":#取消收藏
                    collection = Collection.objects.get(collected_article=article,blog_user=self.request.user)
                    collection.delete()
                    result = 4
                    verb = "取消收藏"
                    action_object = collection
                    description = "collection"
                notify.send(
                    self.request.user,
                    recipient=recipient,
                    verb=verb,
                    target=article,
                    action_object=action_object,
                    description=description
                )
            except Exception as e:
                print(e)
            return JsonResponse(
                {"result":result}
            )
class ArticleEditView(CreateView):
    form_class = ArticleEditForm
    template_name = "blogs/editarticle/editArticle.html"
    def form_valid(self, form):
        article_form = form.save(False)
        article_form.author =  self.request.user
        pre_save.connect(refresh_cache_signals_save_articles,sender=Artical)
        article_form.save(True)
        url = reverse("blog:index")
        return HttpResponseRedirect(url)

    def form_invalid(self, form):
        form.fields["title"].initial = form.cleaned_data["title"]
        form.fields["status"].initial = form.cleaned_data["status"]
        error_message=""
        try:
            form.fields["body"].initial = form.cleaned_data["body"]
        except KeyError as e:
            error_message = "文章内容不能为空"

        return self.render_to_response(
            {
                "form": form,
                "error_message":error_message
            }
        )

class ArticleUpdateVuew(UpdateView):
    form_class = ArticleEditForm
    template_name = "blogs/updateArticle.html"
    model = Artical
    def get(self, request, *args, **kwargs):
        get_type = request.GET.get("type")
        pk = kwargs["pk"]
        if get_type == "remove":
            pre_delete.connect(refresh_cache_signals_delete_articles,sender=Artical)
            Artical.objects.get(pk=pk).delete()

            return HttpResponseRedirect(reverse(
                "blog:manageArticle"
            ))
        elif get_type=="draw":
            article = Artical.objects.get(pk=pk)
            article.status = "d"
            article.save()

            return HttpResponseRedirect(reverse(
                "blog:manageArticle"
            ))
        elif get_type == "express":
            article = Artical.objects.get(pk=pk)
            article.status = "e"
            article.save()
            return HttpResponseRedirect(reverse(
                "blog:manageArticle"
            ))
        else:
            return super(ArticleUpdateVuew,self).get(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateVuew,self).get_context_data(**kwargs)
        pk = self.request.GET.get("pk")
        context["pk"] = pk
        return context

# @method_decorator(cache_page(60*60*24),name="dispatch")
class PersonaBlogView(BaseArticleView):
    template_name = 'blogs/person.html'
    key_prefix = "blog/person/personalArticle-{}-{}"
    model = Artical
    paginate_by = 8
    def get_cache_key(self,username):
        return self.key_prefix.format(username)
    def get_follower_list(self,username):
        follower_list = []
        user = BlogUser.objects.get(username=username)
        follower = Attention.objects.filter(user_id=user)
        self.set_cache_data(("follower-users", username), follower)
        for f in follower:
            users = BlogUser.objects.filter(username=f.B_follower)
            for u in users:
                follower_list.append(u)
        return follower_list
    def get_queryset(self):
        get_type = self.request.GET.get("type")
        username = self.request.GET.get("username")
        follower_list = []
        if not username:
            user = self.request.user
            username = user.username
        else:
            user = BlogUser.objects.get(username=username)
        if not get_type:
            articles = self.get_cache_data(("articles",username))
            if not articles:
                articles = Artical.objects.filter(author=user)
                time = datetime.datetime.now() - datetime.timedelta(days=2)
                articles = articles.filter(pub_time__gte=time)
                self.set_cache_data(("articles",username),articles)
            return articles
        else:
            get_type = int(get_type)
            if get_type == 1:
                follower_list = self.get_cache_data(("attention-follower-user",username))
                follower_list = follower_list if follower_list else []
                if not follower_list:
                    follower_list = self.get_follower_list(username)
                return follower_list
            elif get_type == 2:
                follower_list = self.get_cache_data(("attention-fans-user",username))
                follower_list = follower_list if follower_list else []
                if not follower_list:
                    fans = Attention.objects.filter(B_follower=user)
                    for f in fans:
                        users = BlogUser.objects.filter(username=f.user)
                        for u in users:
                            follower_list.append(u)
                return follower_list
            elif get_type == 3:
                pass
            elif get_type == 4:
                collection_list = self.get_cache_data(("collections-article",username))
                collection_list = collection_list if collection_list else []
                if not collection_list:
                    collection = Collection.objects.filter(blog_user=user)
                    collection_list = []
                    for col in collection:
                        collection_list.append(Artical.objects.get(pk=col.collected_article_id))
                return collection_list
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

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

        get_type = self.request.GET.get("type")
        username = self.request.GET.get("username")
        if not username:
            user = self.request.user
        else:
            user = BlogUser.objects.get(username=username)
        follower_list = self.get_cache_data(("main-attention-follower_list",self.request.user.username))
        follower_list = follower_list if follower_list else []
        if not follower_list:
            follower_list = self.get_follower_list(self.request.user.username)
            self.set_cache_data(("main-attention-follower_list",self.request.user.username),follower_list)
        if get_type:
            get_type = int(get_type)
        info = {}
        """
        get_type 为空，显示最新动态
        get_type 为1，显示关注用户列表
        get_type 为2，显示f粉丝用户列表
        get_type 为3，显示随笔列表
        get_type 为4，显示收藏列表
        """
        articles = self.get_cache_data(("all_articles",username))
        if not articles:
            articles = Artical.objects.filter(author=user)
            self.set_cache_data(("all_articles",username),articles)
        if get_type == 3:
            self.object_list = articles
        context = self.get_context_data()
        person_character_count = 0
        person_article_count = len(articles)

        if get_type==1:
            for u in context["object_list"]:
                follower_count = Attention.objects.filter(user=u).count()
                collection_count = Collection.objects.filter(blog_user=u).count()
                article = Artical.objects.filter(author=u)
                character_count = 0
                for a in article:
                    character_count += len(a.body)
                article_count = len(article)
                info[u.username] = {"follower_count": follower_count,
                                    "collection_count": collection_count,
                                    "character_count": character_count,
                                    "article_count": article_count}
            context["info"] = info
        elif get_type == 2:
            for u in context["object_list"]:
                follower_count = Attention.objects.filter(user=u).count()
                collection_count = Collection.objects.filter(blog_user=u).count()
                article = Artical.objects.filter(author=u)
                character_count = 0
                for a in article:
                    character_count += len(a.body)
                article_count = len(article)
                info[u.username] = {"follower_count": follower_count,
                                    "collection_count": collection_count,
                                    "character_count": character_count,
                                    "article_count": article_count}
            context["info"] = info
        for a in articles:
            person_character_count+=len(a.body)
        context["person_character_count"] = person_character_count
        context["person_article_count"] = person_article_count
        context["user"] = user
        context["type"] = get_type
        context["follower_list"] = follower_list
        return self.render_to_response(context)

class ArticleManagerView(BaseArticleView):
    template_name = "blogs/editarticle/article_manager.html"
    model = Artical
    key_prefix = "article-manager-{}-{}"
    def get_queryset(self):
        author = self.request.user
        articles = self.get_cache_data(("articles",author.username))
        if not articles:
            articles = Artical.objects.filter(author=author)
            self.set_cache_data(("articles",author.username),articles)
        get_type = self.request.GET.get("type")
        if not get_type:
            return articles
        else:
            get_type = int(get_type)
            if get_type == 1:
                articles=articles.order_by("-pub_time")#时间降序
            elif get_type == 2:
                articles=articles.order_by("pub_time")#时间升序
            elif get_type == 3:
                articles=articles.order_by("-thumb_up")#点赞数降序
            elif get_type == 4:
                articles=articles.order_by("thumb_up")#点赞数升序
            elif get_type == 5:
                articles=articles.order_by("-views")#阅读量降序
            elif get_type == 6:
                articles=articles.order_by("views")#阅读量升序
        return articles



class MySearchView(SearchView):
    """My custom search view."""
    template_name = "search/search.html"
    form_class = MySearchForm
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        return super(MySearchView,self).get(request,*args,**kwargs)
    def get_queryset(self):
        queryset = super(MySearchView,self).get_queryset()
        return queryset.all()
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        users  = []
        articles = []
        user = BlogUser.objects.get(username=self.request.user.username)
        followers = user.user.all()
        for s in context["object_list"]:
            if s.model_name == "bloguser":
                users.append(s)
            elif s.model_name == "artical":
                articles.append(s)

        context["users"] = users

        context["articles"] = articles
        context["followers"] = followers
        return context
@never_cache
def refresh_cache(request):
    try:
        url = reverse("blog:index")
        if request.user:
            if cache:
                cache.clear()
                url = reverse("blog:index")
                return HttpResponseRedirect(url)
        else:
            return HttpResponse("the cache is not empty and can't be cleared "
                                "please click <a href='" + url+ "'>this"
                                                                 "</a> to go back!!")
    except Exception as e:
        logger.error(e)
