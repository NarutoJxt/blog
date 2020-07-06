import json

from django import forms
from django.core.cache import cache

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic.edit import FormView,UpdateView
from notifications.signals import notify

from account.models import BlogUser
from comment.form import CommentForm
from comment.models import Comment
from blogs.models import Artical


class CommentListView(FormView):
    form_class = CommentForm
    template_name = "blogs/article_detail.html"

    def get(self, request, *args, **kwargs):
        article_id = kwargs["article_id"]
        article = Artical.objects.get(pk=article_id)
        url = article.get_absolute_url()
        return HttpResponseRedirect(url+"#comment")
    def form_invalid(self, form):
        article_id = self.kwargs["article_id"]
        article = Artical.objects.get(pk=article_id)
        comment_dict,header = article.get_comment_list()
        return self.render_to_response(
            {
                "form":form,
                "article":article,
                "comment_dict":comment_dict,
                "header":header
            }
        )
    def form_valid(self, form):
        article = form.cleaned_data["article"]
        author = self.request.user
        comment = form.save(False)
        comment.article = article
        comment.author = author
        if form.cleaned_data["parent_comment"]:
            comment.parent_comment = form.cleaned_data["parent_comment"]
        comment.save(True)
        recipient = None
        if comment.parent_comment_id:
            recipient = comment.parent_comment.author
            verb = "中回复了你"
        else:
            recipient = comment.author
            verb = "评论了你的文章"
        notify.send(
                self.request.user,
                recipient=recipient,
                verb='回复了你',
                target=comment.article,
                action_object=comment,
            description="comment"
            )
        return HttpResponseRedirect(article.get_absolute_url()+"#comment")
class CommentUpdate(UpdateView):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            body = request.body.decode()
            body = json.loads(body)
            comment_id =int(body["comment_id"])
            thumb_up = int(body["thumb_up"])
            comment = Comment.objects.get(pk=comment_id)
            comment.thumb_up_count = thumb_up
            comment.save()
            return HttpResponse(request.body)

