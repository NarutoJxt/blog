#! /usr/bin/[ython
# -*- coding=utf-8 -*-
import random

from django import template
from django.conf import settings
from django.db.models import Q

from account.models import BlogUser, Attention
from blogs.form import MySearchForm
from blogs.models import Artical
from collection.models import Collection
import re

register = template.Library()
@register.inclusion_tag("base/header.html")
def load_head(request,user):
    img_path = None
    if str(user) != "AnonymousUser":
        img_path = settings.MEDIA_URL+"/"+ str(user.head_path)
    else:
        user = None
    form = MySearchForm()
    return {
        "img_path":img_path,
        "user":user,
        "form":form,
        "request":request
    }
@register.inclusion_tag("base/sidebar.html")
def load_sidebar_info(user):
    article_list = Artical.objects.filter(status="e")
    article_lenght = len(article_list)
    recommended_list = []
    if article_lenght <= 5:
        recommended_list = article_list
    else:
        for i in range(5):
            index = random.randrange(article_lenght)
            while article_list[index] in recommended_list:
                index = random.randrange(article_lenght)
            recommended_list.append(article_list[index])
    user = BlogUser.objects.get(username=user)
    author_list = user.user.all()
    author_list = [author.B_follower.username for author in author_list]
    author_list = BlogUser.objects.exclude(Q(username__in=author_list)|
                                           Q(is_superuser=True)|Q(username=user.username))
    author_list_length = len(author_list)
    follower_list = []
    user = BlogUser.objects.get(username=user.username)
    followers = user.user.all()
    for f in followers:
        follower_list.append(BlogUser.objects.get(username=f.B_follower))
    if author_list_length > 5:
        author_list = author_list[0:5]
    return {
        'recommended_list':recommended_list,
        "author_list":author_list,
        "follower_list":follower_list
    }
@register.inclusion_tag("blogs/person-sidebar.html")
def load_pserson_siderbar(author,user):
    drafts = Artical.objects.filter(status="d",author__username=user.username)
    collections = Collection.objects.filter(blog_user=author)
    result = False
    if user == author:
        result = True
    return {
        "drafts":drafts,
        "collections":collections,
        "user":author,
        "result":result
    }
@register.inclusion_tag("base/detail-sidebar.html")
def load_detail_sidebar_info(user,is_show,is_follower):
    article_list = Artical.objects.filter(status="e")
    article_lenght = len(article_list)
    recommended_list = []
    if article_lenght < 5:
        recommended_list = article_list
    else:
        for i in range(5):
            index = random.randrange(article_lenght)
            recommended_list.append(article_list[index])
    user_article_list = Artical.objects.filter(author=user)
    user_article_list_length = len(user_article_list)
    user_image = user.head_path
    if user_article_list_length > 5:
        author_list = user_article_list[0:5]
    return {
        'recommended_list':recommended_list,
        "user_article_list":user_article_list,
        "user_image": user_image,
        "author":user,
        "is_show":is_show,
        "is_follower":is_follower
    }

@register.filter(name="toString")
def img_to_string(value):
    value = settings.MEDIA_URL+str(value)
    return value
@register.filter(name="connect")
def connect_str(value,arg1):
    value = str(value) + str(arg1)
    return value
@register.filter(name="get_follower_count")
def get_follower_count(info,username):
    return info[username]["follower_count"]
@register.filter(name="get_collection_count")
def get_collection_count(info,username):
    return info[username]["collection_count"]
@register.filter(name="get_character_count")
def get_character_count(info,username):
    return info[username]["character_count"]
#获取文章数量
@register.filter(name="get_article_count")
def get_article_count(info,username):
    return info[username]["article_count"]
#加载左侧sidbar
@register.inclusion_tag("blogs/editarticle/left-sidebar.html")
def load_person_info(user,key):
    img_path = None
    if str(user) != "AnonymousUser":
        img_path = settings.MEDIA_URL + "/" + str(user.head_path)
    else:
        user = None
    return {
        "img_path": img_path,
        "user": user,
        "key":key
    }
@register.filter(name="get_text")
def get_text(artcle):
    artcle = re.sub(u"\<.*?\>","",artcle)
    return artcle
@register.filter(name="get_img")
def get_img(article):
    img = re.findall(r'img src="(.*?)"',article,re.S)
    if len(img) > 0:
        return img[0]
    else:
        return ""
@register.filter(name="check_follower")
def check_follower(follower,followers):
    for f in followers:
        if follower == f.username:
            return False
    return True