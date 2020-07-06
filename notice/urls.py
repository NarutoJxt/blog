#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include

from notice.views import NoticeListView, NoticeUpdateView

app_name = "notice"
urlpatterns = [
    path("show/",NoticeListView.as_view(),name="show"),
    path("update/",NoticeUpdateView.as_view(),name="update")
]