#! /usr/bin/[ython
# -*- coding=utf-8 -*-
from django import template

from account.models import BlogUser, Attention

register = template.Library()
@register.inclusion_tag("attention/attention.html")
def load_attention(user):
    follower = Attention.objects.filter(user=user)
    follower_list = []
    for f in follower:
        users = BlogUser.objects.filter(username=f.B_follower)
        for u in users:
            follower_list.append(u)
    return {
        "follower_list":follower_list,
        "user":user
    }
@register.filter("cover_email")
def cover_email(email):
    email = email.split("@")
    email[0] = list(email[0])
    email[0][-4:] = "****"
    email[0] = "".join(email[0])
    email = "@".join(email)
    return email