from django.db import models

# Create your models here.
from django.utils.timezone import now

from account.models import BlogUser
from blogs.models import Artical


class Compliment(models.Model):
    article = models.ForeignKey(Artical,verbose_name="被点赞的文章",on_delete=models.CASCADE)
    blog_user = models.ForeignKey(BlogUser,verbose_name="点赞者",on_delete=models.DO_NOTHING)
    praise_time = models.DateTimeField(verbose_name="点赞时间",auto_now=now)