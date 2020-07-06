#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from blogs.views import IndexView, Article_Detail, PersonaBlogView, refresh_cache, \
    ArticleEditView, ArticleUpdateVuew, ArticleDealView, MySearchView,ArticleManagerView

app_name = "blog"
urlpatterns = [
   path(r"",IndexView.as_view(),name="index"),
    path(r"article/<int:year>/<int:month>/<int:day>/<int:article_id>.html",Article_Detail.as_view(),name="article_detail"),
    path(r"person//",PersonaBlogView.as_view(),name="person"),
    path(r"refresh_cache/",refresh_cache,name="refresh"),
    path("editArticle/",ArticleEditView.as_view(),name="editArticle"),
    path("updateArticle/<int:pk>.html",ArticleUpdateVuew.as_view(),name="updateArticle"),
    path("dealArticle/", csrf_exempt(ArticleDealView.as_view()),name="ArticleDeal"),
    path("manageArticle/",ArticleManagerView.as_view(),name="manageArticle"),
    path(r"search/",MySearchView.as_view(),name="search"),

]