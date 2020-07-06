#! /usr/bin/[ython
# -*- coding=utf-8 -*-
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, forms, UserCreationForm, UserChangeForm
from django.forms import widgets, ModelForm

from account.models import BlogUser

User = get_user_model()


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(
            attrs={"placeholder": "请输入用户名或邮箱", "class": "form-control", "id": "showImg", "onblur": "changeImg(this)"}

        )
        self.fields["password"].widget = widgets.PasswordInput(
            attrs={"placeholder": "请输入密码", "class": "form-control"}
        )




class ReRegisterForm(ModelForm):
    password1 = forms.CharField(max_length=255)
    username = forms.CharField(max_length=50,min_length=8)
    def __init__(self, *args, **kwargs):
        super(ReRegisterForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = widgets.PasswordInput(
            attrs={"placeholder": "请输入新密码", "class": "form-control"}
        )
        self.fields["password1"].widget = widgets.PasswordInput(
            attrs={"placeholder": "请再次输入密码", "class": "form-control"}
        )
        self.fields["username"].widget = widgets.HiddenInput()
    class Meta:
        model = BlogUser
        fields = ["username", "password", "password1"]


class RegisterForm(UserCreationForm):
    email = forms.CharField(max_length=50)
    head_image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(
            attrs={"placeholder": "用户名为8-16个字符，由字母，数字，其他字符组成", "class": "form-control"}
        )

        self.fields["email"].widget = widgets.EmailInput(
            attrs={"placeholder": "请输入可用的邮箱", "class": "form-control"}
        )
        self.fields["password1"].widget = widgets.PasswordInput(
            attrs={"placeholder": "请输入密码，长度超过8", "class": "form-control"}
        )
        self.fields["password2"].widget = widgets.PasswordInput(
            attrs={"placeholder": "请再次输入密码", "class": "form-control"}
        )
        self.fields["head_image"].widget = widgets.FileInput(
            attrs={
                "style": "position: relative;left: 70px",
                "onchange": "upload(this)"
            }
        )
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "两次密码不一致",
                code='password_mismatch',
            )
        return password2
    def clean_username(self):
        username = self.cleaned_data["username"]
        is_numver = 0
        is_alpha = 0
        is_other = 0
        if len(username)<8:
            raise forms.ValidationError(
                "用户名太短了",
                code="username_length"
            )
        elif len(username) > 16:
            raise forms.ValidationError(
                "用户名太长了",
                code="username_length"
            )
        else:
            for u in username:
                if u.isdigit():
                    is_numver = 1
                elif u.isalpha():
                    is_alpha = 1
                else:
                    is_other = 1
            if is_alpha+is_numver+is_other >= 2:
                return username
            else:
                raise forms.ValidationError(
                    "用户名至少包括字母，数字，其他字符两种以上",
                    code="username_cha"
                )

    class Meta(UserCreationForm.Meta):
        model = BlogUser
        fields = ["username", "email", "head_image"]
        error_messages = {
            "username":{
                "required":"请输入用户昵称",
                "unique":"该用户名已存在",
                "max_length":"输入的用户名过长",
            },
            "email":{
                "required":"邮箱不能为空",
                "unique":"邮箱已存在"
            }
        }

class PersonInfoForm(ModelForm):
    class Meta:
        model = BlogUser
        fields = ["username","head_path","signature","gender","birth_date",
                  "person_instruction"]
        widgets = {
            "head_path":widgets.FileInput(
                attrs={
                    "id":"file",
                    "onchange":"upload(this)"
                }
            ),
            "gender":widgets.RadioSelect(),
            "birth_date":widgets.SelectDateWidget(
                attrs={
                    "style":"width:100px;height:60px;text-align;center;margin-right:10px"
                }
            ),

        }
#基础设置表单
class BaseInfoForm(ModelForm):
    class Meta:
        model = BlogUser
        fields = ["is_access","reveiver_area"]
        widgets = {
            "is_access":widgets.RadioSelect(),
            "reveiver_area":widgets.RadioSelect()
        }