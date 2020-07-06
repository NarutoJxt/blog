import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, ListView
from notifications.signals import notify

from account.models import BlogUser
from blogs.models import Artical
from blogs.views import BaseArticleView, IndexView
from collection.models import Collection
@method_decorator(login_required,name="dispatch")
@method_decorator(csrf_exempt,name="dispatch")
class ShowCollectionView(BaseArticleView):
    template_name = "blogs/person.html"
    model = Collection

    def get_queryset(self):
        user = self.request.user
        collection = Collection.objects.filter(blog_user=user)
        collections = [col.collected_article for col in collection]
        return collections
    def get_context_data(self, *, object_list=None, **kwargs):
        collections = self.get_queryset()
        img_path = cache.get("img_path", None)
        try:
            user = self.request.user
        except KeyError as e:
            pass
        else:
            img_path = settings.MEDIA_URL+"/"+str(user.head_path)
        kwargs["img_path"] = img_path
        kwargs["page"], kwargs["indexs"], kwargs["count"], kwargs["page_allowed"] = self.get_page(collections)
        return super(ShowCollectionView,self).get_context_data(**kwargs)

@method_decorator(csrf_exempt,name="dispatch")

class UpdateCollectionView(UpdateView):
    model = Collection
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        result = ""
        if self.request.is_ajax():
            body = request.body.decode("utf-8")
            body = json.loads(body)
            is_collected = int(body["is_collected"])
            title = body["article"]
            title = title.strip()
            user = self.request.user
            article = Artical.objects.get(title=title)
            recipient = article.author
            verb = ""
            if is_collected == 0:
                collecion = Collection.objects.filter(blog_user=user,collected_article=article)
                if collecion:
                    collecion.delete()
                    result = "已取消收藏"
                    verb = "取消收藏"
                else:
                    result = 0
            elif is_collected == 1:
                collection = Collection(collected_article=article,blog_user=user)
                collection.save()

                result = "收藏成功！！"
                verb = "收藏"
        notify.send(
            self.request.user,
            recipient=recipient,
            verb='回复了你',
            target=article,
            action_object=collecion,
            description="collection"
        )
        return JsonResponse(
            {"result":result}
        )
