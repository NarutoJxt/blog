#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include

from comment.views import CommentListView,CommentUpdate
app_name = "comment"
urlpatterns = [
    path(r"comment/<int:article_id>/postcomment.html/",CommentListView.as_view(),name="postcomment"),
    path(r"comment/postthumb_up.html/",CommentUpdate.as_view(),name="postthumb")
]
