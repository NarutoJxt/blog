#! /usr/bin/[ython
# -*- coding=utf-8 -*-

from haystack import  indexes

from blogs.models import Artical


class ArticalIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr="body")
    def get_model(self):
        return Artical

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status="e")
