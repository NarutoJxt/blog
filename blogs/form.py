#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms
from django.db.models import Q
from django.forms import widgets, ModelForm,HiddenInput
from django.urls import reverse
from froala_editor.widgets import FroalaEditor
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
import haystack.inputs

from account.models import BlogUser
from blogs.models import Artical
from comment.models import Comment


class TitleSearchForm(SearchForm):
    title = forms.CharField(required=True,widget=forms.TextInput(attrs={"placeholder": "title", "class": "form-control"
                                                                        }))
class ArticleEditForm(ModelForm):
    class Meta:
        model = Artical
        fields = ["title","body","status"]
        options = {
            "width": "900",
            "height": "500",
            "toolbarButtons":
                [
                    'bold', 'italic', 'underline', "quote",'insertImage',
                    'insertLink', 'undo', 'redo',"getPDF","fontAwesome",
                    "emoticons","spellChecker","selectAll","fullscreen",
                    "codeBeautifierOptions","indent","paragraphFormat","charCounterCount",
                   "textColor","backgroundColor"
                ],
            "lineHeights": {
                '1.15': '1.15',
                '1.5': '1.5',
                "Double": '2'
            },
            "quickInsertButtons": [
                "image","emoticons",
            ],
            "imageDefaultDisplay":"block",
            "placeholderText":"写下你想要分享的内容",
            "pastePlain":True
        }
        widgets = {
            "body":FroalaEditor(
                theme="dark",
                options=options,
            ),
            "title":forms.TextInput(
                attrs={
                    "style":"width:900px;height:6em;outline:none;border:none;font-size:20px",
                    "placeholder":"请输入标题",
                    "class":"form-control"
                },
            ),
            "status":forms.Select(
                attrs={
                    "style":"height:50px",
                    "class":"form-control"
                }
            )
        }
class ArticleUpdateForm(ModelForm):
    class Meta:
        model = Artical
        fields = ["title","body","status"]
class MySearchForm(SearchForm):
    q = forms.CharField(required=False,
                        widget=forms.TextInput(attrs={
                            'type': 'search',
                            "style":"text-shadow: 0 0 0 black;color: grey;width: 150px;background-color:white",

                            "class":"form-control" ,
                            "placeholder":"Search"
                                                      }
                                               ))
    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = SearchQuerySet().auto_query(self.cleaned_data["q"]).load_all()
        if not self.is_valid():
            return self.no_query_found()
        return sqs


