#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.urls import path, include

from collection.views import UpdateCollectionView,  ShowCollectionView

app_name = "collection"
urlpatterns = [
    path(r"collected.html/",UpdateCollectionView.as_view(),name="collected"),
    path(r"collection.html/",ShowCollectionView.as_view(),name="collection"),
    ]