from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.utils.timezone import now

from account.models import BlogUser
from blogs.models import Artical


class Comment(models.Model):
    body = RichTextField("正文",max_length=300,config_name="comment")
    pub_time = models.DateTimeField(auto_now_add=now)
    author = models.ForeignKey(BlogUser,verbose_name="作者",on_delete=models.CASCADE)
    article = models.ForeignKey(Artical,verbose_name="文章",on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self",verbose_name="上级评论",null=True,blank=True,on_delete=models.CASCADE)
    class Meta:
        ordering = ["pub_time"]
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = "pub_time"
    def __str__(self):
        return self.body
