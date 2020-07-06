#! /usr/bin/[ython
# -*- coding=utf-8 -*-

from haystack import  indexes

from account.models import BlogUser
from blogs.models import Artical


class BlogUserIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')
    is_superuser = indexes.IntegerField(model_attr="is_superuser")
    def get_model(self):
        return BlogUser

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(is_superuser=True)
