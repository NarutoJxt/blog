#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django.forms import ModelForm
from django import forms

from comment.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["body","article","parent_comment"]
        widgets = {
            "body":forms.Textarea(attrs={
                "class":"form-control",
                "placeholder":"white you want to say!!!"
               },
            ),
            "parent_comment":forms.HiddenInput(
                attrs={
                    "id":"parent_comment_id"
                }
            ),
        }