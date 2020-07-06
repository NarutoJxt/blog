from django.db import models

# Create your models here.
from django.utils.timezone import now

from account.models import BlogUser
from blogs.models import Artical


class Collection(models.Model):
    collected_time = models.DateTimeField(verbose_name="收藏时间", auto_now=now)
    blog_user = models.ForeignKey(to=BlogUser,verbose_name="收藏者",on_delete=models.DO_NOTHING,related_name="collection")
    collected_article = models.ForeignKey(Artical,verbose_name="收藏的文章",on_delete=models.CASCADE,related_name="article")
    class Meta:
        ordering = ["-collected_time"]
        verbose_name = "收藏表"
