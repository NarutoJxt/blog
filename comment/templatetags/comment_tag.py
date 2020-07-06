#! /usr/bin/[ython
# -*- coding=utf-8 -*-

from django import template

from comment.models import Comment

register = template.Library()
@register.inclusion_tag("comment/comment_list.html")
def get_comment_list(article):
    comment_list = Comment.objects.filter(article=article)
    count = Comment.objects.filter(article=article).count()
    return {
        "comment_list":comment_list,
        "count":count,
        "article_id":article.pk
    }
@register.filter(name="judge_empty")
def judge_empty(comment_dict,comment):
    if len(comment_dict[comment]) > 0:
        return True
    else:
        return False
@register.inclusion_tag("comment/comment_tree.html")
def get_comment_tree(comment,comment_dict):
    comments = comment_dict[comment]
    return {
        "comments":comments,
        "comment_dict":comment_dict
    }
