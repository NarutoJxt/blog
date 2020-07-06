from django.db import models

# Create your models here.
from blogs.models import Artical


class AppealArticleModel(models.Model):
    APPEAL_OPTIONS = [
        ("色情低俗","色情低俗"),
        ("违法乱纪","违法乱纪"),
        ("言语恶毒","言语恶毒"),
        ("广告或垃圾信息","广告或垃圾信息"),
        ("抄袭","抄袭"),
        ("其他","其他")
    ]


    appeal_options = models.CharField(max_length=60,verbose_name="申诉选项",choices=APPEAL_OPTIONS)
    appealed_article = models.ForeignKey(to=Artical,on_delete=models.DO_NOTHING)
    appeal_body = models.TextField(max_length=500,blank=True,null=True,verbose_name="申诉内容")
    class Meta:
        db_table = "投诉"
        verbose_name = "投诉"