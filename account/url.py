#! /usr/bin/[ython
# -*- coding=utf-8 -*-

from django.urls import path
from account.views import LoginView, RegisterView, LogoutView, getImg, ReRegisterView, edit_signature, \
    PersonInfoView, BaseInfoView, get_code, update_email, modify_password, deal_attention, AttentionView

app_name = "account"
urlpatterns = [
    path(r"login/",LoginView.as_view(),name="login"),
    path(r"register/",RegisterView.as_view(),name="register"),
    path(r"logout/",LogoutView.as_view(),name="logout"),
    path(r"showImg/",getImg,name="showImg"),
    path(r"re_register/",ReRegisterView.as_view(),name="re_register"),
    path(r"attention/",deal_attention,name="attention"),
    path(r"editSignature/",edit_signature,name="editSignature"),
    path(r"set_person_info/<int:pk>.html",PersonInfoView.as_view(),name="set_person_info"),
    path(r"base_info/<int:pk>.html",BaseInfoView.as_view(),name="get_base_info"),
    path(r"get_code/",get_code,name="get_code"),
    path("update_email/",update_email,name="update_email"),
    path('modify_pwd/',modify_password,name="modify_pwd"),
    path("friend_loop/",AttentionView.as_view(),name="friend_loop")
]
