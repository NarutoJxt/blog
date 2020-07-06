from django.db import models

# Create your models here.
from django.utils.timezone import now

from Blog import settings
from account.models import BlogUser


class OauthUser(models.Model):
    user_alternative_type = (
        ("1","github"),
        ("2","google"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                             null=True,blank=True)
    openid = models.CharField(default="",max_length=100,unique=True)
    user_type = models.CharField(max_length=20,choices=user_alternative_type)
    nickname = models.CharField(max_length=150,verbose_name="昵称")
    tocken = models.CharField(max_length=255,blank=True,null=True)
    picture = models.CharField(max_length=150,blank=True,null=True)
    email = models.EmailField(max_length=50,default="")
    create_time = models.DateTimeField(verbose_name="创建时间",default=now)
    last_mod_time = models.DateTimeField(verbose_name="修改时间",default=now)
    def __str__(self):
        return self.nickname
    class Meta:
        verbose_name = "oauth用户"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]
class OauthConfig(models.Model):
    user_alternative_type = (
        ("github","github"),
        ("google","google"),
    )
    type = models.CharField(max_length=150,choices=user_alternative_type,
                            default="github")
    app_key = models.CharField(max_length=200,verbose_name="AppKey")
    app_secret = models.CharField(max_length=200,verbose_name="AppSecret")
    callBack_url = models.URLField(max_length=255,verbose_name="回调地址",
                                   default="http://127.0.0.1:8000/")
    create_time = models.DateTimeField(verbose_name="创建时间", default=now)
    last_mod_time = models.DateTimeField(verbose_name="修改时间", default=now)
    is_enable = models.BooleanField(verbose_name="是否显示",default=True)
    class Meta:
        verbose_name = "oauth配置"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]