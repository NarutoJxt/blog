from django.contrib import admin

# Register your models here.
from comment.models import Comment


@admin.register(Comment)
class CommentADmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'body', 'author', 'article', 'pub_time')
    list_display_links = ('id', 'body')
    list_filter = ('author', 'article')
    search_fields = ["author","article","body"]
    date_hierarchy = "pub_time"